"""
Configuración del panel administrativo para el módulo de usuarios.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import FormularioRegistro
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Configuración personalizada del admin para Usuario."""

    add_form = FormularioRegistro
    model = Usuario
    list_display = (
        "email",
        "nombre",
        "apellido",
        "es_activo",
        "es_staff",
        "fecha_registro",
    )
    list_filter = ("es_activo", "es_staff", "is_superuser")
    search_fields = ("email", "nombre", "apellido")
    ordering = ("-fecha_registro",)

    fieldsets = (
        ("Credenciales", {"fields": ("email", "password")}),
        ("Información personal", {"fields": ("nombre", "apellido")}),
        (
            "Permisos",
            {
                "fields": (
                    "es_activo",
                    "es_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Fechas", {"fields": ("fecha_registro", "last_login")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "nombre",
                    "apellido",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    readonly_fields = ("fecha_registro", "last_login")
