"""
Modelos del módulo de usuarios.
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UsuarioManager


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado que usa el email
    como identificador principal en lugar de username.
    """

    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico",
    )
    nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre",
    )
    apellido = models.CharField(
        max_length=150,
        verbose_name="Apellido",
    )
    es_activo = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )
    es_staff = models.BooleanField(
        default=False,
        verbose_name="Staff",
    )
    fecha_registro = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de registro",
    )

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre", "apellido"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["-fecha_registro"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Retorna el nombre completo del usuario."""
        return f"{self.nombre} {self.apellido}".strip()

    def get_short_name(self):
        """Retorna el nombre corto del usuario."""
        return self.nombre

    @property
    def is_active(self):
        return self.es_activo

    @property
    def is_staff(self):
        return self.es_staff
