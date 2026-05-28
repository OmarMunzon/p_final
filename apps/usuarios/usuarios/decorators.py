"""
Decoradores de control de acceso por rol.

Uso:
    @solo_estudiantes
    def mi_vista(request): ...

    @solo_profesores
    def mi_vista(request): ...
"""

from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def solo_estudiantes(vista):
    """Permite el acceso únicamente a usuarios con rol Estudiante."""
    @wraps(vista)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('usuarios:login')
        if not request.user.es_estudiante:
            messages.error(
                request,
                'Esta sección es exclusiva para estudiantes.',
            )
            return redirect('usuarios:dashboard')
        return vista(request, *args, **kwargs)
    return wrapper


def solo_profesores(vista):
    """Permite el acceso únicamente a usuarios con rol Profesor."""
    @wraps(vista)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('usuarios:login')
        if not request.user.es_profesor:
            messages.error(
                request,
                'Esta sección es exclusiva para profesores.',
            )
            return redirect('usuarios:dashboard')
        return vista(request, *args, **kwargs)
    return wrapper