from django import forms
from django.utils import timezone

from .models import Reserva, Vehiculo, Visita


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'tipo', 'marca', 'modelo', 'color', 'residente', 'activo']

    def clean_placa(self):
        return self.cleaned_data['placa'].strip().upper()


class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['nombres', 'apellidos', 'documento', 'telefono', 'residente', 'observaciones']

    def clean_documento(self):
        return self.cleaned_data['documento'].strip()


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            'zona_comun', 'residente', 'fecha', 'hora_inicio', 'hora_fin',
            'estado', 'observaciones',
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        inicio = cleaned_data.get('hora_inicio')
        fin = cleaned_data.get('hora_fin')
        zona = cleaned_data.get('zona_comun')
        estado = cleaned_data.get('estado')

        if fecha and fecha < timezone.localdate():
            self.add_error('fecha', 'La reserva no puede ser en una fecha pasada.')
        if inicio and fin and inicio >= fin:
            self.add_error('hora_fin', 'La hora de finalización debe ser posterior a la de inicio.')
        if fecha and inicio and fin and zona and estado != Reserva.Estado.CANCELADA:
            conflictos = Reserva.objects.filter(
                zona_comun=zona,
                fecha=fecha,
                estado__in=[Reserva.Estado.PENDIENTE, Reserva.Estado.APROBADA],
                hora_inicio__lt=fin,
                hora_fin__gt=inicio,
            )
            if self.instance.pk:
                conflictos = conflictos.exclude(pk=self.instance.pk)
            if conflictos.exists():
                raise forms.ValidationError(
                    'Ya existe una reserva activa que se cruza con ese horario.'
                )
        return cleaned_data
