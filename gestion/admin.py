from django.contrib import admin

from .models import Reserva, Vehiculo, Visita


admin.site.register(Vehiculo)
admin.site.register(Visita)
admin.site.register(Reserva)
