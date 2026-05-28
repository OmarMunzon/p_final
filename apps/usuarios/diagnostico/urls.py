"""
URLs del módulo de diagnóstico.
"""

from django.urls import path

from . import views

app_name = "diagnostico"

urlpatterns = [
    path("", views.vista_inicio_diagnostico, name="inicio"),
    path("pregunta/<int:numero>/", views.vista_pregunta, name="pregunta"),
    path("resultado/<int:pk>/", views.vista_resultado, name="resultado"),
    path("historial/", views.vista_historial, name="historial"),
    path("reiniciar/", views.vista_reiniciar, name="reiniciar"),
]
