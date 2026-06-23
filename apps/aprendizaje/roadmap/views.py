import json
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.urls import reverse

from .evaluator import (
    calculate_score,
    evaluate_code,
    evaluate_fill,
    evaluate_quiz,
)
from .judge0 import run_code
from .models import (
    RoadmapExercise, 
    RoadmapLesson, 
    RoadmapStage,
    RoadmapUserProgress, 
    RoadmapUserXP,
    RoadmapLessonProgress
)
from .services.adaptive_service import ejecutar_adaptacion



@login_required
def roadmap_view(request):
    stages = RoadmapStage.objects.prefetch_related('lessons__exercises').all()
    xp_profile = None
    
    usuario_id = request.user.id
    perfil = request.user.perfil_estudiante
    nivel = perfil.get_nombre_nivel()
    
    # Determinar cuántas lecciones desbloquear según el nivel
    match nivel:
        case 'easy':
            # Nivel fácil: desbloquear TODAS las lecciones disponibles
            max_lessons_to_unlock = 1
        case 'medium':
            # Nivel medio: desbloquear primeras 5 lecciones
            max_lessons_to_unlock = 5
        case 'hard':
            # Nivel difícil: desbloquear solo primera lección
            max_lessons_to_unlock = float('inf')
        case _:
            max_lessons_to_unlock = 0
    
    # Contar lecciones desbloqueadas y establecer status
    lessons_unlocked = 0
    for stage in stages:
        for lesson in stage.lessons.all():
            # Si la lección ya está completada, dejarla así
            # if lesson.status == 'completed':
            #     continue
            lesson_progress, _ = RoadmapLessonProgress.objects.get_or_create(
                user=request.user,
                lesson=lesson,
                defaults={
                    'status': 'locked'
                }
            )

            lesson.progress = lesson_progress

            if lesson_progress.status == 'completed':
                continue
            
            
            if lessons_unlocked < max_lessons_to_unlock:

                if lesson_progress.status == 'locked':
                    lesson_progress.status = 'available'
                    lesson_progress.save()

                lessons_unlocked += 1

            else:

                if lesson_progress.status != 'completed':
                    lesson_progress.status = 'locked'
                    lesson_progress.save()

    if request.user.is_authenticated:
        xp_profile, _ = RoadmapUserXP.objects.get_or_create(user=request.user)
    
    return render(request, 'roadmap/roadmap.html', {
        'stages':     stages,
        'xp_profile': xp_profile,        
        'estudent_level': nivel,
    })


@login_required
def exercise_view(request, exercise_id):
    exercise    = get_object_or_404(RoadmapExercise, pk=exercise_id)
    progress, _ = RoadmapUserProgress.objects.get_or_create(
        user=request.user, exercise=exercise,
    )
    #print(f"Progreso: {progress}")
    next_ex = RoadmapExercise.objects.filter(
        lesson=exercise.lesson,
        order__gt=exercise.order,
    ).first()

    return render(request, 'roadmap/exercise.html', {
        'exercise':       exercise,
        'test_cases':     exercise.test_cases.filter(is_hidden=False),
        'progress':       progress,
        'next_exercise':  next_ex,
        'attempts_left':  max(0, exercise.max_attempts - progress.attempts),
        'starter_code':   progress.last_code or exercise.starter_code,
        'fill_parts':     exercise.get_fill_parts(),
        'quiz_questions': exercise.quiz_questions.all()
                          if exercise.exercise_type == 'quiz' else [],
    })


@login_required
@require_POST
def run_exercise_view(request, exercise_id):
    exercise = get_object_or_404(RoadmapExercise, pk=exercise_id)
    data     = json.loads(request.body)
    result   = run_code(data.get('code', ''), language='python')
    return JsonResponse({
        'stdout':    result['stdout'],
        'stderr':    result['stderr'],
        'status':    result['status'],
        'exec_time': result.get('time'),
    })


@login_required
@require_POST
def submit_exercise_view(request, exercise_id):
    
    exercise    = get_object_or_404(RoadmapExercise, pk=exercise_id)
    progress, _ = RoadmapUserProgress.objects.get_or_create(
        user=request.user, exercise=exercise,
    )

    if progress.solved:
        return JsonResponse({'status': 'already_solved', 'all_passed': True})
    if progress.attempts >= exercise.max_attempts:
        return JsonResponse({'status': 'no_attempts', 'all_passed': False})

    data       = json.loads(request.body)
    time_spent = data.get('time_spent', 0)

    # ── Evaluar según tipo ──
    if exercise.exercise_type == 'code':
        user_code  = data.get('code', '')
        results    = evaluate_code(exercise, user_code)
        all_passed = all(r['passed'] for r in results if not r['is_hidden'])
        progress.last_code = user_code

    elif exercise.exercise_type == 'fill':
        user_answers        = data.get('answers', [])
        results, answers_ok = evaluate_fill(exercise, user_answers)
        all_passed          = answers_ok or all(
            r['passed'] for r in results if not r['is_hidden']
        )

    elif exercise.exercise_type == 'quiz':
        user_answer = data.get('answer', {})
        # print(f"Respuestas del usuario para el ejercicio {exercise_id}: {user_answers}") ok
        results      = evaluate_quiz(exercise, user_answer)
        all_passed   = all(r['passed'] for r in results)

    else:
        return JsonResponse({'status': 'unknown_type'}, status=400)

    progress.attempts  += 1
    progress.time_spent = time_spent

    xp = 0
    next_exercise_url = None # nuevo agregado

    adaptacion = None
    intento = None
    if all_passed:
        xp                 = calculate_score(exercise, progress.attempts, time_spent, True)
        progress.solved    = True
        adaptacion = ejecutar_adaptacion(request.user)
        
        # if adaptacion.get("siguiente_ejercicio"):

        #     next_exercise_url = reverse(
        #         "roadmap:exercise",
        #         args=[
        #             adaptacion[
        #                 "siguiente_ejercicio"
        #             ].id
        #         ]
        #     )
        progress.xp_earned = xp

        # Guardar antes de contar
        progress.save()

        # Buscar siguiente ejercicio de la misma lección
        next_exercise = RoadmapExercise.objects.filter(
            lesson=exercise.lesson,
            order__gt=exercise.order
        ).order_by('order').first()
        #).first()

        # Si existe siguiente ejercicio
        if next_exercise:
            next_exercise_url = reverse(
                'roadmap:exercise',
                args=[next_exercise.id]
            )

        # Sumar XP al perfil del usuario
        xp_profile, _ = RoadmapUserXP.objects.get_or_create(user=request.user)
        xp_profile.total_xp += xp
        xp_profile.save()

        # Desbloquear siguiente lección si todos los ejercicios están resueltos
        lesson   = exercise.lesson
        total_exercises = lesson.exercises.count()

        # Guardamos el progreso actual primero para que cuente en la siguiente consulta
        #progress.save()

        solved_exercises = RoadmapUserProgress.objects.filter(
            user=request.user,
            exercise__lesson=lesson,
            solved=True,
        ).count()

        # if solved_exercises == total_exercises:
        #     lesson.status = 'completed'
        #     lesson.save()

        #     next_lesson = RoadmapLesson.objects.filter(
        #         stage=lesson.stage,
        #         order__gt=lesson.order,
        #     ).order_by('order').first()
        #     #).first()
        #     if next_lesson and next_lesson.status == 'locked':
        #         next_lesson.status = 'available'
        #         next_lesson.save()
        if solved_exercises == total_exercises:

            lesson_progress, _ = RoadmapLessonProgress.objects.get_or_create(
                user=request.user,
                lesson=lesson,
                defaults={
                    'status': 'available'
                }
            )

            lesson_progress.status = 'completed'
            lesson_progress.completed_at = timezone.now()
            lesson_progress.save()

            next_lesson = RoadmapLesson.objects.filter(
                stage=lesson.stage,
                order__gt=lesson.order,
            ).order_by('order').first()

            if next_lesson:

                next_progress, _ = RoadmapLessonProgress.objects.get_or_create(
                    user=request.user,
                    lesson=next_lesson,
                    defaults={
                        'status': 'locked'
                    }
                )

                if next_progress.status == 'locked':
                    next_progress.status = 'available'
                    next_progress.save()
    else:
        # Si NO pasó, guardamos el intento fallido en la BD
        progress.save()

    # Respuesta con adaptación incluida
    response_data = {
        'status':            'correct' if all_passed else 'incorrect',
        'all_passed':        all_passed,
        'results':           [r for r in results if not r.get('is_hidden', False)],
        'attempts':          progress.attempts,
        'attempts_left':     max(0, exercise.max_attempts - progress.attempts),
        'xp_earned':         xp,
        'next_exercise_url': next_exercise_url,
    }
    
    # Agregar adaptación solo si se resolvió correctamente
    if adaptacion:
        response_data["adaptacion"] = {
            "prediccion": adaptacion["prediccion"],
            "feedback": adaptacion["feedback"],
            "siguiente_ejercicio":
                adaptacion[
                    "siguiente_ejercicio"
                ].id
                if adaptacion[
                    "siguiente_ejercicio"
                ]
                else None
        }
    
    return JsonResponse(response_data)


@login_required
def progress_view(request):
    """
    Vista de progreso del usuario que muestra:
    - XP total y racha
    - Ejercicios completados y precisión
    - Progreso por etapa/lección
    - Actividad reciente
    """
    initialize_user_roadmap(request.user)

    # ─── Obtener perfil XP ───
    xp_profile, _ = RoadmapUserXP.objects.get_or_create(user=request.user)
    
    # ─── Obtener todas las etapas con lecciones ───
    stages = RoadmapStage.objects.prefetch_related(
        'lessons__exercises__roadmapuserprogress_set'
    ).all()
    
    # ─── Cálcular estadísticas generales ───
    # Ejercicios completados
    completed_exercises = RoadmapUserProgress.objects.filter(
        user=request.user,
        solved=True,
    ).count()
    
    # Total de ejercicios en el sistema
    total_exercises = RoadmapExercise.objects.count()
    
    # Precisión: ejercicios resueltos en 1er intento vs intentados
    first_attempt_solved = RoadmapUserProgress.objects.filter(
        user=request.user,
        attempts=1,
        solved=True,
    ).count()
    
    attempted_exercises = RoadmapUserProgress.objects.filter(
        user=request.user,
    ).count()
    
    accuracy = 0
    if attempted_exercises > 0:
        accuracy = round((first_attempt_solved / attempted_exercises) * 100)
    
    # NUEVO
    completed_lessons = RoadmapLessonProgress.objects.filter(
        user=request.user,
        status='completed'
    ).count()

    # Lecciones completadas
    # completed_lessons = RoadmapLesson.objects.filter(
    #     status='completed'
    # ).count()
    
    # ─── Enriquecer datos de etapas ───
    for stage in stages:
        for lesson in stage.lessons.all():

            # NUEVO
            lesson.progress, _ = RoadmapLessonProgress.objects.get_or_create(
                user=request.user,
                lesson=lesson,
                defaults={
                    'status': 'locked'
                }
            )

            # Contar ejercicios completados en esta lección
            lesson_exercises = lesson.exercises.count()
            lesson_solved = RoadmapUserProgress.objects.filter(
                user=request.user,
                exercise__lesson=lesson,
                solved=True,
            ).count()
            
            lesson.total_exercises = lesson_exercises
            lesson.completed_exercises = lesson_solved
            lesson.progress_percentage = (
                round((lesson_solved / lesson_exercises) * 100) 
                if lesson_exercises > 0 else 0
            )
    
    # ─── Actividad reciente (últimas 10 actualizaciones de progreso) ───
    recent_activity = RoadmapUserProgress.objects.filter(
        user=request.user,
    ).select_related('exercise__lesson__stage').order_by('-updated_at')[:10]
    
    context = {
        'xp_profile': xp_profile,
        'stages': stages,
        'user_progress': completed_exercises,
        'total_exercises': total_exercises,
        'accuracy': accuracy,
        'completed_lessons': completed_lessons,
        'recent_activity': recent_activity,
        'attempted_exercises': attempted_exercises,
    }
    return render(request, 'roadmap/progress.html', context)



def initialize_user_roadmap(user):

    first_lesson = RoadmapLesson.objects.order_by(
        'stage__order',
        'order'
    ).first()

    if first_lesson:

        RoadmapLessonProgress.objects.get_or_create(
            user=user,
            lesson=first_lesson,
            defaults={
                'status': 'available'
            }
        )

