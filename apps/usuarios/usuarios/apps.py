"""
Configuración de la aplicación Usuarios.
"""

from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    """Configuración del módulo de usuarios."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.usuarios.usuarios"
    verbose_name = "Usuarios"
