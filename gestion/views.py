from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ReservaForm, VehiculoForm, VisitaForm
from .models import Reserva, Vehiculo, Visita


def inicio(request):
    return render(request, 'gestion/inicio.html', {
        'vehiculos_activos': Vehiculo.objects.filter(activo=True).count(),
        'visitas_activas': Visita.objects.filter(estado=Visita.Estado.EN_CONJUNTO).count(),
        'reservas_hoy': Reserva.objects.filter(fecha=timezone.localdate()).count(),
    })


def vehiculos(request):
    return render(request, 'gestion/lista.html', {
        'titulo': 'Vehículos',
        'accion': 'vehiculos',
        'objetos': Vehiculo.objects.select_related('residente', 'residente__vivienda'),
    })


def crear_vehiculo(request):
    form = VehiculoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Vehículo registrado correctamente.')
        return redirect('vehiculos')
    return render(request, 'gestion/formulario.html', {
        'titulo': 'Registrar vehículo', 'form': form, 'volver': 'vehiculos',
    })


def visitas(request):
    return render(request, 'gestion/lista.html', {
        'titulo': 'Visitas',
        'accion': 'visitas',
        'objetos': Visita.objects.select_related('residente', 'residente__vivienda'),
    })


def crear_visita(request):
    form = VisitaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Entrada de visita registrada correctamente.')
        return redirect('visitas')
    return render(request, 'gestion/formulario.html', {
        'titulo': 'Registrar visita', 'form': form, 'volver': 'visitas',
    })


def finalizar_visita(request, visita_id):
    visita = get_object_or_404(Visita, pk=visita_id)
    if request.method == 'POST' and visita.estado == Visita.Estado.EN_CONJUNTO:
        visita.estado = Visita.Estado.FINALIZADA
        visita.fecha_salida = timezone.now()
        visita.save(update_fields=['estado', 'fecha_salida'])
        messages.success(request, 'Salida de visita registrada correctamente.')
    return redirect('visitas')


def reservas(request):
    return render(request, 'gestion/lista.html', {
        'titulo': 'Reservas',
        'accion': 'reservas',
        'objetos': Reserva.objects.select_related('residente', 'residente__vivienda'),
    })


def crear_reserva(request):
    form = ReservaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Reserva registrada correctamente.')
        return redirect('reservas')
    return render(request, 'gestion/formulario.html', {
        'titulo': 'Registrar reserva', 'form': form, 'volver': 'reservas',
    })


def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    if request.method == 'POST' and reserva.estado != Reserva.Estado.CANCELADA:
        reserva.estado = Reserva.Estado.CANCELADA
        reserva.save(update_fields=['estado'])
        messages.success(request, 'Reserva cancelada correctamente.')
    return redirect('reservas')
