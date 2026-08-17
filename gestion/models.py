from django.db import models


class Vehiculo(models.Model):
    class Tipo(models.TextChoices):
        AUTOMOVIL = 'Automovil', 'Automóvil'
        MOTO = 'Moto', 'Moto'
        BICICLETA = 'Bicicleta', 'Bicicleta'
        OTRO = 'Otro', 'Otro'

    placa = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    marca = models.CharField(max_length=50, blank=True)
    modelo = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=30, blank=True)
    residente = models.ForeignKey(
        'residentes.Residente',
        on_delete=models.PROTECT,
        db_column='id_residente',
        related_name='vehiculos',
    )
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vehiculos'
        ordering = ['placa']

    def __str__(self):
        return self.placa


class Visita(models.Model):
    class Estado(models.TextChoices):
        EN_CONJUNTO = 'EN_CONJUNTO', 'En conjunto'
        FINALIZADA = 'FINALIZADA', 'Finalizada'

    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    documento = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20, blank=True)
    residente = models.ForeignKey(
        'residentes.Residente',
        on_delete=models.PROTECT,
        db_column='id_residente',
        related_name='visitas',
    )
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=15,
        choices=Estado.choices,
        default=Estado.EN_CONJUNTO,
    )
    observaciones = models.TextField(blank=True)

    class Meta:
        db_table = 'visitas'
        ordering = ['-fecha_entrada']

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'


class Reserva(models.Model):
    class Zona(models.TextChoices):
        SALON_COMUNAL = 'Salon comunal', 'Salón comunal'
        BBQ = 'Zona BBQ', 'Zona BBQ'
        PISCINA = 'Piscina', 'Piscina'
        CANCHA = 'Cancha', 'Cancha'
        OTRO = 'Otro', 'Otro'

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        APROBADA = 'APROBADA', 'Aprobada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    zona_comun = models.CharField(max_length=40, choices=Zona.choices)
    residente = models.ForeignKey(
        'residentes.Residente',
        on_delete=models.PROTECT,
        db_column='id_residente',
        related_name='reservas',
    )
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(
        max_length=12,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    observaciones = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reservas'
        ordering = ['fecha', 'hora_inicio']

    def __str__(self):
        return f'{self.zona_comun} - {self.fecha}'
