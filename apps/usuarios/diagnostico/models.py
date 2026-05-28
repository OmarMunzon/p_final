"""
Modelos del módulo de diagnóstico.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone


class Diagnostico(models.Model):
    """
    Registro de cada respuesta dada por el estudiante
    durante su evaluación diagnóstica inicial.
    """

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diagnosticos",
        verbose_name="Estudiante",
    )
    enunciado = models.TextField(
        verbose_name="Enunciado de la pregunta",
    )
    respuesta_correcta = models.CharField(
        max_length=500,
        verbose_name="Respuesta correcta",
    )
    respuesta_usuario = models.CharField(
        max_length=500,
        blank=True,
        default="",
        verbose_name="Respuesta del estudiante",
    )
    es_correcta = models.BooleanField(
        default=False,
        verbose_name="¿Respuesta correcta?",
    )
    puntaje_obtenido = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Puntaje obtenido",
    )
    fecha = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de respuesta",
    )

    class Meta:
        verbose_name = "Diagnóstico"
        verbose_name_plural = "Diagnósticos"
        ordering = ["-fecha"]

    def __str__(self):
        return (
            f"{self.usuario.email} — "
            f"{self.enunciado[:50]} — "
            f"{self.puntaje_obtenido} pts"
        )


class Historial(models.Model):
    """
    Agrupa todos los registros de un diagnóstico completo
    realizado por un estudiante en una sola sesión.
    """

    NIVELES = [
        ("principiante", "Principiante"),
        ("intermedio", "Intermedio"),
        ("avanzado", "Avanzado"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="historiales",
        verbose_name="Estudiante",
    )
    puntaje_total = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Puntaje total",
    )
    nivel_asignado = models.CharField(
        max_length=20,
        choices=NIVELES,
        blank=True,
        default="",
        verbose_name="Nivel asignado",
    )
    total_preguntas = models.PositiveIntegerField(
        default=0,
        verbose_name="Total de preguntas",
    )
    respuestas_correctas = models.PositiveIntegerField(
        default=0,
        verbose_name="Respuestas correctas",
    )
    fecha_inicio = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de inicio",
    )
    fecha_fin = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de finalización",
    )
    completado = models.BooleanField(
        default=False,
        verbose_name="Completado",
    )
    diagnosticos = models.ManyToManyField(
        Diagnostico,
        blank=True,
        verbose_name="Preguntas respondidas",
    )

    class Meta:
        verbose_name = "Sesión de diagnóstico"
        verbose_name_plural = "Sesiones de diagnóstico"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return (
            f"{self.usuario.email} — "
            f'{self.fecha_inicio.strftime("%d/%m/%Y")} — '
            f"{self.puntaje_total} pts"
        )

    @property
    def porcentaje_acierto(self):
        """Calcula el porcentaje de respuestas correctas."""
        if self.total_preguntas == 0:
            return 0
        return round((self.respuestas_correctas / self.total_preguntas) * 100, 2)

    def calcular_nivel(self):
        """Asigna el nivel según el puntaje obtenido."""
        pct = self.porcentaje_acierto
        if pct >= 75:
            return "avanzado"
        elif pct >= 45:
            return "intermedio"
        return "principiante"
