"""
Vistas del módulo de residentes.

Contiene las operaciones necesarias para consultar
y registrar residentes.
"""

from django.shortcuts import redirect, render

from .models import Residente, Vivienda


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

        vivienda = Vivienda.objects.get(
            pk=id_vivienda
        )

        Residente.objects.create(
            nombres=nombres,
            apellidos=apellidos,
            correo=correo,
            telefono=telefono,
            tipo_residente=tipo_residente,
            titular=titular,
            documento=documento,
            vivienda=vivienda
        )

        return redirect('listar_residentes')

    return render(
        request,
        'residentes/crear.html',
        {
            'viviendas': viviendas
        }
    )