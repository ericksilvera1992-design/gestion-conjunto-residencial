import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('residentes', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zona_comun', models.CharField(choices=[('Salon comunal', 'Salón comunal'), ('Zona BBQ', 'Zona BBQ'), ('Piscina', 'Piscina'), ('Cancha', 'Cancha'), ('Otro', 'Otro')], max_length=40)),
                ('fecha', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('APROBADA', 'Aprobada'), ('CANCELADA', 'Cancelada')], default='PENDIENTE', max_length=12)),
                ('observaciones', models.TextField(blank=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('residente', models.ForeignKey(db_column='id_residente', on_delete=django.db.models.deletion.PROTECT, related_name='reservas', to='residentes.residente')),
            ],
            options={'db_table': 'reservas', 'ordering': ['fecha', 'hora_inicio']},
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=10, unique=True)),
                ('tipo', models.CharField(choices=[('Automovil', 'Automóvil'), ('Moto', 'Moto'), ('Bicicleta', 'Bicicleta'), ('Otro', 'Otro')], max_length=20)),
                ('marca', models.CharField(blank=True, max_length=50)),
                ('modelo', models.CharField(blank=True, max_length=20)),
                ('color', models.CharField(blank=True, max_length=30)),
                ('activo', models.BooleanField(default=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('residente', models.ForeignKey(db_column='id_residente', on_delete=django.db.models.deletion.PROTECT, related_name='vehiculos', to='residentes.residente')),
            ],
            options={'db_table': 'vehiculos', 'ordering': ['placa']},
        ),
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=80)),
                ('apellidos', models.CharField(max_length=80)),
                ('documento', models.CharField(max_length=20)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('fecha_entrada', models.DateTimeField(auto_now_add=True)),
                ('fecha_salida', models.DateTimeField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('EN_CONJUNTO', 'En conjunto'), ('FINALIZADA', 'Finalizada')], default='EN_CONJUNTO', max_length=15)),
                ('observaciones', models.TextField(blank=True)),
                ('residente', models.ForeignKey(db_column='id_residente', on_delete=django.db.models.deletion.PROTECT, related_name='visitas', to='residentes.residente')),
            ],
            options={'db_table': 'visitas', 'ordering': ['-fecha_entrada']},
        ),
    ]
