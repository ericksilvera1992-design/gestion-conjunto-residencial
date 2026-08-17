"""
Vistas del módulo de residentes.

Este módulo contiene las vistas encargadas de consultar
y mostrar la información de los residentes.
"""

from django.shortcuts import render

from .models import Residente


def listar_residentes(request):
    """
    Obtiene los residentes registrados y los envía a la plantilla.

    Args:
        request: Solicitud HTTP recibida por Django.

    Returns:
        HttpResponse: Página con la lista de residentes.
    """
    residentes = Residente.objects.all().order_by(
        'nombres',
        'apellidos'
    )

    return render(
        request,
        'residentes/listar.html',
        {
            'residentes': residentes
        }
    )