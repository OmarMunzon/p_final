"""
URL raíz del proyecto.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.usuarios.usuarios.urls", namespace="usuarios")),
    path(  # ← agregar esto
        "diagnostico/",
        include("apps.usuarios.diagnostico.urls", namespace="diagnostico"),
    ),
    path(                                          # ← solo esto es nuevo
        'aprendizaje/',
        include('apps.aprendizaje.roadmap.urls', namespace='roadmap'),
    ),
    path(                                          # ← esto es nuevo
        'seguimiento/',
        include('apps.seguimiento.urls', namespace='seguimiento'),
    ),
]
