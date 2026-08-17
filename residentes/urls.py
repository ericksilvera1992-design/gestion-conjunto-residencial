"""
Rutas del módulo de residentes.

Este módulo define las URLs relacionadas con la gestión
y consulta de residentes.
"""

from django.urls import path

from . import views


urlpatterns = [
    path(
        '',
        views.listar_residentes,
        name='listar_residentes'
    ),

    path(
        'crear/',
        views.crear_residente,
        name='crear_residente'
    ),
]