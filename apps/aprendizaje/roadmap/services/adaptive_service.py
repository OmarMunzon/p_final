from apps.modelo.predictor import recomendar
from apps.modelo.feedback import generar_feedback

from apps.aprendizaje.roadmap.models import (
    RoadmapExerciseAttempt,
    RoadmapUserProgress,    
    RoadmapLessonProgress,
    RoadmapExercise,
)


def obtener_siguiente_ejercicio(usuario, prediccion):    
    mapa_dificultad = {
        "Reforzar": "easy",
        "Mantener": "medium",
        "Avanzar": "hard"
    }

    dificultad = mapa_dificultad.get(
        prediccion,
        "medium"
    )

    ejercicios_resueltos = (
        RoadmapUserProgress.objects
        .filter(
            user=usuario,
            solved=True
        )
        .values_list(
            "exercise_id",
            flat=True
        )
    )

    siguiente = (
        RoadmapExercise.objects
        .filter(
            difficulty=dificultad
        )
        .exclude(
            id__in=ejercicios_resueltos
        )
        .order_by("id")
        .first()
    )

    return siguiente


def calcular_estadisticas(usuario):

    progresos = RoadmapUserProgress.objects.filter(
        user=usuario
    )

    ejercicios_resueltos = progresos.count() 

    ejercicios_correctos = progresos.filter(
        solved=True
    ).count()

    porcentaje_aciertos = 0

    if ejercicios_resueltos > 0:

        porcentaje_aciertos = (
            ejercicios_correctos
            / ejercicios_resueltos
        ) * 100
    
    intentos_totales = sum(
        p.attempts
        for p in progresos
    )

    # intentos_promedio = (
    #     intentos_totales / ejercicios_resueltos
    #     if ejercicios_resueltos
    #     else 0
    # )
    
    tiempo_promedio = (
        sum(p.time_spent for p in progresos)
        / ejercicios_resueltos
        if ejercicios_resueltos
        else 0
    )

    xp = 0

    
    if hasattr(usuario, "roadmap_xp"):
        xp = usuario.roadmap_xp.total_xp

    
    perfil = usuario.perfil_estudiante

    return {
        "edad": 0,

        "curso": 0,            

        "nivel_diagnostico":
            perfil.nivel_actual,

        "tema_actual": 1,

        "ejercicios_resueltos":
            ejercicios_resueltos,

        "porcentaje_aciertos":
            porcentaje_aciertos,

        "intentos_promedio":
            3,

        "tiempo_promedio_seg":
            tiempo_promedio,

        "errores_consecutivos":
           calcular_errores_leccion_actual(usuario),

        "xp_acumulada":
            xp,

        "lecciones_completadas":
            RoadmapLessonProgress.objects.filter(
                user=usuario,
                status="completed"
            ).count(),

        "dias_inactividad":
            0
    }


def ejecutar_adaptacion(usuario):

    print("ENTRO A ADAPTACION")
    
    try:
        datos = calcular_estadisticas(usuario)
        print("DATOS:", datos)

    except Exception as e:
        print("ERROR CALCULANDO ESTADISTICAS")
        print(type(e))
        print(e)
        raise

    prediccion = recomendar(
        # edad=datos["edad"],
        # curso=datos["curso"],
        nivel_diagnostico=datos["nivel_diagnostico"],
        # tema_actual=datos["tema_actual"],
        ejercicios_resueltos=datos["ejercicios_resueltos"],
        porcentaje_aciertos=datos["porcentaje_aciertos"],
        intentos_promedio=datos["intentos_promedio"],
        # tiempo_promedio_seg=datos["tiempo_promedio_seg"],
        errores_consecutivos=datos["errores_consecutivos"],
        xp_acumulada=datos["xp_acumulada"],
        lecciones_completadas=datos["lecciones_completadas"],
        # dias_inactividad=datos["dias_inactividad"]
    )

    feedback = generar_feedback(
        prediccion
    )
    
    print("prediccion ",prediccion)
    print("feedback ",feedback)
    
    siguiente = obtener_siguiente_ejercicio(
        usuario,
        prediccion
    )

    return {
        "prediccion": prediccion,
        "feedback": feedback,
        "siguiente_ejercicio": siguiente
    }
   

def calcular_errores_consecutivos(usuario):

    intentos = (
        RoadmapExerciseAttempt.objects
        .filter(user=usuario)
        .order_by("-created_at")
    )

    errores = 0

    for intento in intentos:

        if intento.is_correct:
            break

        errores += 1

    return errores

def calcular_errores_leccion_actual(usuario):
    # 1. Obtenemos el último intento realizado por el usuario
    ultimo_intento = (
        RoadmapExerciseAttempt.objects
        .filter(user=usuario)
        .order_by("-created_at")
        .first()
    )

    # Si el usuario no ha intentado ningún ejercicio, sus errores son 0
    if not ultimo_intento:
        return 0

    # 2. Identificamos la lección actual a través de ese último ejercicio
    # (Asumiendo que 'exercise' tiene una relación con la lección mediante 'lesson_id' o 'lesson')
    leccion_actual_id = ultimo_intento.exercise.lesson_id

    # 3. Contamos todos los errores del usuario dentro de los ejercicios de esa lección
    errores_leccion_actual = (
        RoadmapExerciseAttempt.objects
        .filter(
            user=usuario,
            is_correct=False,
            exercise__lesson_id=leccion_actual_id  # Filtra los ejercicios que comparten esta lección
        )
        .count()
    )

    return errores_leccion_actual