"""
Configuración de las URLs principales del proyecto Lucrier.

Este archivo conecta las rutas generales del proyecto
con las diferentes aplicaciones de Django.
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas del módulo de residentes.
    path(
        'residentes/',
        include('residentes.urls')
    ),
    path('', include('gestion.urls')),
]
