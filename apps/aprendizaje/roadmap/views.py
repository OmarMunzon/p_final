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
    RoadmapExercise, RoadmapLesson, RoadmapStage,
    RoadmapUserProgress, RoadmapUserXP,
)


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
            if lesson.status == 'completed':
                continue
            
            # Si aún no hemos alcanzado el límite y no está completada, desbloquear
            if lessons_unlocked < max_lessons_to_unlock:
                lesson.status = 'available'
                lessons_unlocked += 1
            else:
                # Resto de lecciones: bloquear
                lesson.status = 'locked'
            
            lesson.save()

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
    if all_passed:
        xp                 = calculate_score(exercise, progress.attempts, time_spent, True)
        progress.solved    = True
        progress.xp_earned = xp

        # Buscar siguiente ejercicio de la misma lección
        next_exercise = RoadmapExercise.objects.filter(
            lesson=exercise.lesson,
            order__gt=exercise.order
        ).first()

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
        all_done = not RoadmapUserProgress.objects.filter(
            user=request.user,
            exercise__lesson=lesson,
            solved=False,
        ).exists()
        if all_done:
            lesson.status = 'completed'
            lesson.save()
            next_lesson = RoadmapLesson.objects.filter(
                stage=lesson.stage,
                order__gt=lesson.order,
            ).first()
            if next_lesson and next_lesson.status == 'locked':
                next_lesson.status = 'available'
                next_lesson.save()

    progress.save()

    return JsonResponse({
        'status':        'correct' if all_passed else 'incorrect',
        'all_passed':    all_passed,
        'results':       [r for r in results if not r.get('is_hidden', False)],
        'attempts':      progress.attempts,
        'attempts_left': max(0, exercise.max_attempts - progress.attempts),
        'xp_earned':     xp,
         # NUEVO
        'next_exercise_url': next_exercise_url,
    })


@login_required
def progress_view(request):
    """
    Vista de progreso del usuario que muestra:
    - XP total y racha
    - Ejercicios completados y precisión
    - Progreso por etapa/lección
    - Actividad reciente
    """
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
    
    # Lecciones completadas
    completed_lessons = RoadmapLesson.objects.filter(
        status='completed'
    ).count()
    
    # ─── Enriquecer datos de etapas ───
    for stage in stages:
        for lesson in stage.lessons.all():
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


