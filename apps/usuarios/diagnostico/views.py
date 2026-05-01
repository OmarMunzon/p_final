"""
Vistas del módulo de diagnóstico.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .data import PREGUNTAS_DIAGNOSTICO, PUNTAJE_MAXIMO
from .models import Diagnostico, SesionDiagnostico


@login_required
def vista_inicio_diagnostico(request):
    """
    Muestra la pantalla de bienvenida del diagnóstico
    y verifica si el usuario ya lo completó.
    """
    sesion_previa = SesionDiagnostico.objects.filter(
        usuario=request.user,
        completado=True,
    ).order_by('-fecha_inicio').first()

    contexto = {
        'titulo': 'Diagnóstico Inicial',
        'sesion_previa': sesion_previa,
        'total_preguntas': len(PREGUNTAS_DIAGNOSTICO),
    }
    return render(request, 'diagnostico/inicio.html', contexto)


@login_required
def vista_pregunta(request, numero):
    """
    Muestra una pregunta del diagnóstico y procesa la respuesta.
    El número va de 1 a N (cantidad de preguntas).
    """
    total = len(PREGUNTAS_DIAGNOSTICO)

    if numero < 1 or numero > total:
        return redirect('diagnostico:inicio')

    sesion_id = request.session.get('sesion_diagnostico_id')
    if not sesion_id:
        sesion = SesionDiagnostico.objects.create(
            usuario=request.user,
            total_preguntas=total,
        )
        request.session['sesion_diagnostico_id'] = sesion.id
    else:
        sesion = get_object_or_404(
            SesionDiagnostico,
            id=sesion_id,
            usuario=request.user,
        )

    if sesion.completado:
        return redirect('diagnostico:resultado', pk=sesion.pk)

    pregunta_data = PREGUNTAS_DIAGNOSTICO[numero - 1]

    if request.method == 'POST':
        respuesta_usuario = request.POST.get('respuesta', '').strip()
        es_correcta = (
            respuesta_usuario == pregunta_data['respuesta_correcta']
        )
        puntaje = pregunta_data['puntaje'] if es_correcta else 0

        diagnostico = Diagnostico.objects.create(
            usuario=request.user,
            enunciado=pregunta_data['enunciado'],
            respuesta_correcta=pregunta_data['respuesta_correcta'],
            respuesta_usuario=respuesta_usuario,
            es_correcta=es_correcta,
            puntaje_obtenido=puntaje,
        )
        sesion.diagnosticos.add(diagnostico)

        if es_correcta:
            sesion.respuestas_correctas += 1
        sesion.puntaje_total += puntaje
        sesion.save()

        if numero == total:
            sesion.nivel_asignado = sesion.calcular_nivel()
            sesion.fecha_fin = timezone.now()
            sesion.completado = True
            sesion.save()

            if 'sesion_diagnostico_id' in request.session:
                del request.session['sesion_diagnostico_id']

            return redirect('diagnostico:resultado', pk=sesion.pk)

        return redirect('diagnostico:pregunta', numero=numero + 1)

    contexto = {
        'titulo': f'Pregunta {numero} de {total}',
        'pregunta': pregunta_data,
        'numero': numero,
        'total': total,
        'progreso': round((numero - 1) / total * 100),
        'sesion': sesion,
    }
    return render(request, 'diagnostico/pregunta.html', contexto)


@login_required
def vista_resultado(request, pk):
    """Muestra el resultado final del diagnóstico."""
    sesion = get_object_or_404(
        SesionDiagnostico,
        pk=pk,
        usuario=request.user,
    )
    diagnosticos = sesion.diagnosticos.all().order_by('fecha')

    contexto = {
        'titulo': 'Resultado del Diagnóstico',
        'sesion': sesion,
        'diagnosticos': diagnosticos,
        'puntaje_maximo': PUNTAJE_MAXIMO,
        'porcentaje': sesion.porcentaje_acierto,
    }
    return render(request, 'diagnostico/resultado.html', contexto)


@login_required
def vista_historial(request):
    """Muestra el historial de diagnósticos del usuario."""
    sesiones = SesionDiagnostico.objects.filter(
        usuario=request.user,
        completado=True,
    ).order_by('-fecha_inicio')

    contexto = {
        'titulo': 'Historial de Diagnósticos',
        'sesiones': sesiones,
        'puntaje_maximo': PUNTAJE_MAXIMO,
    }
    return render(request, 'diagnostico/historial.html', contexto)


@login_required
@require_POST
def vista_reiniciar(request):
    """Reinicia la sesión de diagnóstico en progreso."""
    sesion_id = request.session.get('sesion_diagnostico_id')
    if sesion_id:
        SesionDiagnostico.objects.filter(
            id=sesion_id,
            usuario=request.user,
            completado=False,
        ).delete()
        del request.session['sesion_diagnostico_id']

    return redirect('diagnostico:inicio')
