"""
Configuración de la aplicación Diagnóstico.
"""

from django.apps import AppConfig


class DiagnosticoConfig(AppConfig):
    """Configuración del módulo de diagnóstico."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.usuarios.diagnostico'
    verbose_name = 'Diagnóstico'
