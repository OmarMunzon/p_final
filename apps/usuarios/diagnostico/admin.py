"""
Configuración del panel administrativo para el módulo de diagnóstico.
"""

from django.contrib import admin

from .models import Diagnostico, SesionDiagnostico


@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    """Admin para registros individuales de diagnóstico."""

    list_display = (
        'usuario',
        'enunciado_corto',
        'es_correcta',
        'puntaje_obtenido',
        'fecha',
    )
    list_filter = ('es_correcta', 'fecha')
    search_fields = ('usuario__email', 'enunciado')
    readonly_fields = (
        'usuario', 'enunciado', 'respuesta_correcta',
        'respuesta_usuario', 'es_correcta',
        'puntaje_obtenido', 'fecha',
    )
    ordering = ('-fecha',)

    def enunciado_corto(self, obj):
        """Muestra los primeros 60 caracteres del enunciado."""
        return obj.enunciado[:60] + ('...' if len(obj.enunciado) > 60 else '')

    enunciado_corto.short_description = 'Enunciado'


@admin.register(SesionDiagnostico)
class SesionDiagnosticoAdmin(admin.ModelAdmin):
    """Admin para sesiones completas de diagnóstico."""

    list_display = (
        'usuario',
        'puntaje_total',
        'nivel_asignado',
        'respuestas_correctas',
        'total_preguntas',
        'completado',
        'fecha_inicio',
    )
    list_filter = ('nivel_asignado', 'completado', 'fecha_inicio')
    search_fields = ('usuario__email',)
    readonly_fields = (
        'usuario', 'puntaje_total', 'nivel_asignado',
        'total_preguntas', 'respuestas_correctas',
        'fecha_inicio', 'fecha_fin', 'completado',
    )
    ordering = ('-fecha_inicio',)
