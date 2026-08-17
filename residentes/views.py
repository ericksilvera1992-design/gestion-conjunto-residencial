"""
Vistas del módulo de residentes.

Contiene las operaciones necesarias para consultar
y registrar residentes.
"""

from django.shortcuts import redirect, render

from .models import Residente, Vivienda
from backend.controladores.residente_controlador import (
    ResidenteControlador
)


def listar_residentes(request):
    """
    Obtiene los residentes registrados y los muestra
    en la plantilla correspondiente.
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


def crear_residente(request):
    """
    Registra un nuevo residente en la base de datos.

    La información se recibe mediante un formulario POST.
    """
    viviendas = Vivienda.objects.all().order_by(
        'codigo_vivienda'
    )

    if request.method == 'POST':
        nombres = request.POST.get('nombres', '').strip()
        apellidos = request.POST.get('apellidos', '').strip()
        correo = request.POST.get('correo', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        tipo_residente = request.POST.get(
            'tipo_residente',
            ''
        ).strip()
        titular = request.POST.get('titular', '').strip()
        documento = request.POST.get('documento', '').strip()
        id_vivienda = request.POST.get(
            'id_vivienda',
            ''
        ).strip()

        try:
            datos = ResidenteControlador._validar_datos(
                nombres,
                apellidos,
                correo,
                telefono,
                tipo_residente,
                titular,
                documento,
                id_vivienda
            )

            vivienda = Vivienda.objects.get(
                pk=datos['id_vivienda']
            )

            Residente.objects.create(
                nombres=datos['nombres'],
                apellidos=datos['apellidos'],
                correo=datos['correo'],
                telefono=datos['telefono'],
                tipo_residente=datos['tipo_residente'],
                titular=datos['titular'],
                documento=datos['documento'],
                vivienda=vivienda
            )

            return redirect('listar_residentes')

        except ValueError as error:
            return render(
                request,
                'residentes/crear.html',
                {
                    'viviendas': viviendas,
                    'error': str(error),
                    'nombres': nombres,
                    'apellidos': apellidos,
                    'correo': correo,
                    'telefono': telefono,
                    'tipo_residente': tipo_residente,
                    'titular': titular,
                    'documento': documento,
                    'id_vivienda': id_vivienda
                }
            )

        except Vivienda.DoesNotExist:
            return render(
                request,
                'residentes/crear.html',
                {
                    'viviendas': viviendas,
                    'error': 'La vivienda seleccionada no existe.',
                    'nombres': nombres,
                    'apellidos': apellidos,
                    'correo': correo,
                    'telefono': telefono,
                    'tipo_residente': tipo_residente,
                    'titular': titular,
                    'documento': documento,
                    'id_vivienda': id_vivienda
                }
            )

    return render(
        request,
        'residentes/crear.html',
        {
            'viviendas': viviendas
        }
    )