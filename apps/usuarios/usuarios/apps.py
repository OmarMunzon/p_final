"""
Configuración de la aplicación Usuarios.
"""

from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    """Configuración del módulo de usuarios."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.usuarios.usuarios"
    verbose_name = "Usuarios"

    
    def ready(self):
        """Conecta las señales al iniciar la aplicación."""
        import apps.usuarios.usuarios.signals  # noqa: F401
