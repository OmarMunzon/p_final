"""
Manager personalizado para el modelo Usuario.
"""

from django.contrib.auth.models import BaseUserManager

# from .models import Estudiante


class UsuarioManager(BaseUserManager):
    """Manager que usa email como campo de identificación principal."""

    def create_user(
        self,
        email,
        nombre,
        apellido,
        password=None,
        **extra_fields,
    ):
        """Crea y guarda un usuario con email y contraseña."""
        if not email:
            raise ValueError("El correo electrónico es obligatorio.")

        email = self.normalize_email(email)
        usuario = self.model(
            email=email,
            nombre=nombre,
            apellido=apellido,
            **extra_fields,
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(
        self,
        email,
        nombre,
        apellido,
        password=None,
        **extra_fields,
    ):
        """Crea y guarda un superusuario."""
        extra_fields.setdefault("es_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("es_activo", True)

        if extra_fields.get("es_staff") is not True:
            raise ValueError("El superusuario debe tener es_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(
            email,
            nombre,
            apellido,
            password,
            **extra_fields,
        )
