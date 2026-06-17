from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from apps.usuarios.usuarios.models import Usuario, PerfilEstudiante
from apps.aprendizaje.roadmap.models import RoadmapUserProgress, RoadmapExercise

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def vista_estudiantes(request):
    """Panel de seguimiento de estudiantes."""

    contexto = obtener_datos_estudiantes()
    
    return render(
        request,
        "seguimiento/estudiantes.html",
        contexto,
    )


def detalle_estudiante(request, id):
    """
    Muestra el detalle completo de un estudiante.
    """

    contexto = obtener_detalle_estudiante(id)

    return render(
        request,
        "seguimiento/detalle_estudiante.html",
        contexto,
    )


def obtener_datos_estudiantes():
    estudiantes = Usuario.objects.filter(
        rol="estudiante"
    ).order_by('id')

    total_estudiantes = estudiantes.count()

    estudiantes_data = []

    suma_progreso = 0
    suma_precision = 0

    total_exercises = RoadmapExercise.objects.count()

    for estudiante in estudiantes:

        # Perfil
        perfil = PerfilEstudiante.objects.filter(
            usuario=estudiante
        ).first()

        nivel_actual = (
            perfil.nivel_actual
            if perfil
            else "Sin diagnóstico"
        )

        # Progreso
        progresos = RoadmapUserProgress.objects.filter(
            user=estudiante
        )

        completed_exercises = progresos.filter(
            solved=True
        ).count()

        #Cuenta todos los intentos.
        attempted_exercises = progresos.count()

        # Precisión
        if attempted_exercises > 0:
            accuracy = round(
                (completed_exercises / attempted_exercises) * 100,
                2
            )
        else:
            accuracy = 0

        # Porcentaje de avance
        if total_exercises > 0:
            progress_percentage = round(
                (completed_exercises / total_exercises) * 100,
                2
            )
        else:
            progress_percentage = 0

        # Última actividad
        ultima_actividad = (
            progresos.order_by("-updated_at")
            .values_list("updated_at", flat=True)
            .first()
        )

        estudiantes_data.append({
            "id": estudiante.id,
            "nombre": estudiante.nombre,
            "apellido": estudiante.apellido,
            "email": estudiante.email,
            "nivel_actual": nivel_actual,
            "completed_exercises": completed_exercises,
            "total_exercises": total_exercises,
            "accuracy": accuracy,
            "progress_percentage": progress_percentage,
            "last_activity": ultima_actividad,
        })

        suma_progreso += progress_percentage
        suma_precision += accuracy

    # Promedios generales
    if total_estudiantes > 0:
        promedio_progreso = round(
            suma_progreso / total_estudiantes,
            2
        )

        promedio_precision = round(
            suma_precision / total_estudiantes,
            2
        )
    else:
        promedio_progreso = 0
        promedio_precision = 0

    # Estudiantes con actividad
    estudiantes_activos = len([
        e for e in estudiantes_data
        if e["last_activity"]
    ])

    return {
        "total_estudiantes": total_estudiantes,
        "estudiantes_activos": estudiantes_activos,
        "promedio_progreso": promedio_progreso,
        "promedio_precision": promedio_precision,
        "estudiantes": estudiantes_data,
    }


def obtener_detalle_estudiante(id):

    estudiante = get_object_or_404(
        Usuario,
        id=id,
        rol="estudiante"
    )

    perfil = PerfilEstudiante.objects.filter(
        usuario_id=estudiante.id
    ).first()

    progresos = RoadmapUserProgress.objects.filter(
        user=estudiante
    ).order_by("updated_at")#-update_at

    total_intentos = progresos.count()

    ejercicios_resueltos = progresos.filter(
        solved=True
    ).count()

    ejercicios_pendientes = progresos.filter(
        solved=False
    ).count()

    if total_intentos > 0:
        precision = round(
            (ejercicios_resueltos / total_intentos) * 100,
            2
        )
    else:
        precision = 0

    ultima_actividad = (
        progresos.first().updated_at
        if progresos.exists()
        else None
    )

    return {
        "estudiante": estudiante,
        "perfil": perfil,
        "progresos": progresos[:20],
        "ejercicios_resueltos": ejercicios_resueltos,
        "ejercicios_pendientes": ejercicios_pendientes,
        "total_intentos": total_intentos,
        "precision": precision,
        "ultima_actividad": ultima_actividad,
    }
 

def exportar_pdf_estudiantes(request):

    contexto = obtener_datos_estudiantes()

    template = get_template(
        "seguimiento/pdf_estudiantes.html"
    )

    html = template.render(contexto)

    response = HttpResponse(
        content_type="application/pdf"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="estudiantes.pdf"'

    pisa_status = pisa.CreatePDF(
        html,
        dest=response
    )

    if pisa_status.err:
        return HttpResponse(
            "Error al generar PDF",
            status=500
        )

    return response


def exportar_pdf_detalle_estudiante(
    request,
    id
):

    contexto = obtener_detalle_estudiante(id)

    template = get_template(
        "seguimiento/pdf_detalle_estudiante.html"
    )

    html = template.render(contexto)

    response = HttpResponse(
        content_type="application/pdf"
    )

    nombre = (
        f"{contexto['estudiante'].nombre}_"
        f"{contexto['estudiante'].apellido}.pdf"
    )

    response[
        "Content-Disposition"
    ] = f'attachment; filename="{nombre}"'

    pisa_status = pisa.CreatePDF(
        html,
        dest=response
    )

    if pisa_status.err:
        return HttpResponse(
            "Error al generar PDF",
            status=500
        )

    return response