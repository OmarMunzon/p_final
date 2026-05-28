"""
URLs del módulo Roadmap.
"""

from django.urls import path
from . import views

app_name = 'roadmap'

urlpatterns = [
    path(
        '',
        views.roadmap_view,
        name='index',
    ),
    path(
        'ejercicio/<int:exercise_id>/',
        views.exercise_view,
        name='exercise',
    ),
    path(
        'ejercicio/<int:exercise_id>/run/',
        views.run_exercise_view,
        name='run',
    ),
    path(
        'ejercicio/<int:exercise_id>/submit/',
        views.submit_exercise_view,
        name='submit',
    ),
    path(
        'progreso/',
        views.progress_view,
        name='progress',
    ),
]