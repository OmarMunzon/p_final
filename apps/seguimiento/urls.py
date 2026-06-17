from django.urls import path

from . import views

app_name = "seguimiento"

urlpatterns = [
    path('estudiantes/', views.vista_estudiantes , name='index'),
    path(
        "estudiantes/<int:id>/",
        views.detalle_estudiante,
        name="detalle_estudiante"
    ),
    path(
        "estudiantes/pdf/",
        views.exportar_pdf_estudiantes,
        name="exportar_pdf_estudiantes"
    ),
    path(
        "detalle-estudiante/<int:id>/pdf/",
        views.exportar_pdf_detalle_estudiante,
        name="exportar_pdf_detalle_estudiante"
    ),
]