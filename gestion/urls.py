from django.urls import path

from . import views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('vehiculos/', views.vehiculos, name='vehiculos'),
    path('vehiculos/crear/', views.crear_vehiculo, name='crear_vehiculo'),
    path('visitas/', views.visitas, name='visitas'),
    path('visitas/crear/', views.crear_visita, name='crear_visita'),
    path('visitas/<int:visita_id>/finalizar/', views.finalizar_visita, name='finalizar_visita'),
    path('reservas/', views.reservas, name='reservas'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    path('reservas/<int:reserva_id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
]
