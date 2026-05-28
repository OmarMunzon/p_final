"""
Señales del módulo de usuarios.

Crean automáticamente el perfil extendido
(PerfilEstudiante o PerfilProfesor) cada vez que
se registra un nuevo usuario según su rol.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PerfilEstudiante, PerfilProfesor, Usuario


@receiver(post_save, sender=Usuario)
def crear_perfil_segun_rol(sender, instance, created, **kwargs):
    """
    Al crear un nuevo Usuario crea el perfil extendido
    correspondiente a su rol.
    """
    if not created:
        return

    if instance.rol == Usuario.ROL_ESTUDIANTE:
        PerfilEstudiante.objects.get_or_create(usuario=instance)

    elif instance.rol == Usuario.ROL_PROFESOR:
        PerfilProfesor.objects.get_or_create(usuario=instance)


@receiver(post_save, sender=Usuario)
def sincronizar_perfil(sender, instance, created, **kwargs):
    """
    Al actualizar un Usuario existente, si cambia de rol
    crea el nuevo perfil y elimina el anterior si corresponde.
    """
    if created:
        return

    tiene_perfil_estudiante = hasattr(instance, 'perfil_estudiante')
    tiene_perfil_profesor = hasattr(instance, 'perfil_profesor')

    if instance.rol == Usuario.ROL_ESTUDIANTE:
        if not tiene_perfil_estudiante:
            PerfilEstudiante.objects.get_or_create(usuario=instance)
        if tiene_perfil_profesor:
            instance.perfil_profesor.delete()

    elif instance.rol == Usuario.ROL_PROFESOR:
        if not tiene_perfil_profesor:
            PerfilProfesor.objects.get_or_create(usuario=instance)
        if tiene_perfil_estudiante:
            instance.perfil_estudiante.delete()
