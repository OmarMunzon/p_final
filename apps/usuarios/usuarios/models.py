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

    ROL_ESTUDIANTE = "estudiante"
    ROL_PROFESOR = "profesor"

    ROLES = [
        (ROL_ESTUDIANTE, "Estudiante"),
        (ROL_PROFESOR, "Profesor"),
    ]

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
    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default=ROL_ESTUDIANTE,
        verbose_name="Rol",
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

    # ── Verificadores de rol ───────────────────────────────────────────────
    @property
    def es_estudiante(self):
        return self.rol == self.ROL_ESTUDIANTE

    @property
    def es_profesor(self):
        return self.rol == self.ROL_PROFESOR

    def get_perfil(self):
        """
        Retorna el perfil extendido según el rol.
        Devuelve None si el perfil aún no existe.
        """
        if self.es_estudiante:
            return getattr(self, "perfil_estudiante", None)
        if self.es_profesor:
            return getattr(self, "perfil_profesor", None)
        return None


# ---------------------------------------------------------------------------
# Managers filtrados por rol (para proxies y queries limpias)
# ---------------------------------------------------------------------------


class EstudianteManager(UsuarioManager):
    """Manager que filtra solo usuarios con rol estudiante."""

    def get_queryset(self):
        return super().get_queryset().filter(rol=Usuario.ROL_ESTUDIANTE)

    def create_user(self, email, nombre, apellido, password=None, **kw):
        kw["rol"] = Usuario.ROL_ESTUDIANTE
        return super().create_user(email, nombre, apellido, password, **kw)


class ProfesorManager(UsuarioManager):
    """Manager que filtra solo usuarios con rol profesor."""

    def get_queryset(self):
        return super().get_queryset().filter(rol=Usuario.ROL_PROFESOR)

    def create_user(self, email, nombre, apellido, password=None, **kw):
        kw["rol"] = Usuario.ROL_PROFESOR
        return super().create_user(email, nombre, apellido, password, **kw)


# ---------------------------------------------------------------------------
# Modelos proxy (misma tabla, comportamiento diferenciado)
# ---------------------------------------------------------------------------


class Estudiante(Usuario):
    """
    Proxy de Usuario para el rol Estudiante.
    No genera tabla propia; opera sobre la tabla `usuarios_usuario`.
    El perfil extendido (nivel, progreso) vive en PerfilEstudiante.
    """

    objects = EstudianteManager()

    class Meta:
        proxy = True
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def save(self, *args, **kwargs):
        self.rol = Usuario.ROL_ESTUDIANTE
        super().save(*args, **kwargs)

    @property
    def nivel_actual(self):
        perfil = getattr(self, "perfil_estudiante", None)
        return perfil.nivel_actual if perfil else 1

    @property
    def progreso(self):
        perfil = getattr(self, "perfil_estudiante", None)
        return perfil.progreso if perfil else 0.00

    def subir_nivel(self):
        """Sube el nivel del estudiante si no está en el máximo."""
        perfil = getattr(self, "perfil_estudiante", None)
        if perfil:
            perfil.subir_nivel()

    def actualizar_progreso(self, nuevo_progreso):
        """Actualiza el progreso y sube de nivel si llega a 100."""
        perfil = getattr(self, "perfil_estudiante", None)
        if perfil:
            perfil.actualizar_progreso(nuevo_progreso)


class Profesor(Usuario):
    """
    Proxy de Usuario para el rol Profesor.
    No genera tabla propia; opera sobre la tabla `usuarios_usuario`.
    El perfil extendido vive en PerfilProfesor.
    """

    objects = ProfesorManager()

    class Meta:
        proxy = True
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"

    def save(self, *args, **kwargs):
        self.rol = Usuario.ROL_PROFESOR
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Perfiles extendidos (una tabla por rol)
# ---------------------------------------------------------------------------


class PerfilEstudiante(models.Model):
    """
    Perfil extendido para usuarios con rol Estudiante.
    Almacena nivel_actual y progreso.
    Se crea automáticamente al registrar un estudiante.
    """

    NIVELES = [
        (1, "easy"),
        (2, "medium"),
        (3, "hard"),
    ]

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="perfil_estudiante",
        verbose_name="Usuario",
        limit_choices_to={"rol": Usuario.ROL_ESTUDIANTE},
    )
    nivel_actual = models.PositiveIntegerField(
        default=1,
        choices=NIVELES,
        verbose_name="Nivel actual",
    )
    progreso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Progreso (%)",
    )

    class Meta:
        verbose_name = "Perfil de estudiante"
        verbose_name_plural = "Perfiles de estudiantes"

    def __str__(self):
        return (
            f"{self.usuario.get_full_name()} — "
            f"Nivel {self.nivel_actual} — "
            f"{self.progreso}%"
        )

    def get_nombre_nivel(self):
        """Retorna el nombre legible del nivel."""
        return dict(self.NIVELES).get(self.nivel_actual, "Desconocido")

    def subir_nivel(self):
        """Incrementa el nivel si no está en el máximo."""
        if self.nivel_actual < 5:
            self.nivel_actual += 1
            self.progreso = 0.00
            self.save()

    def actualizar_progreso(self, nuevo_progreso):
        """
        Actualiza el progreso. Si llega o supera 100,
        sube de nivel automáticamente.
        """
        if nuevo_progreso >= 100:
            self.subir_nivel()
        else:
            self.progreso = nuevo_progreso
            self.save()


class PerfilProfesor(models.Model):
    """
    Perfil extendido para usuarios con rol Profesor.
    Almacena especialidad, biografía y años de experiencia.
    Se crea automáticamente al registrar un profesor.
    """

    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="perfil_profesor",
        verbose_name="Usuario",
        limit_choices_to={"rol": Usuario.ROL_PROFESOR},
    )

    class Meta:
        verbose_name = "Perfil de profesor"
        verbose_name_plural = "Perfiles de profesores"

    def __str__(self):
        return f"{self.usuario.get_full_name()}"
