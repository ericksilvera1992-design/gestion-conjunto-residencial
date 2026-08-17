import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Vivienda',
            fields=[
                ('id_vivienda', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_vivienda', models.CharField(max_length=20)),
                ('torre', models.CharField(blank=True, max_length=10, null=True)),
                ('codigo_vivienda', models.CharField(max_length=20, unique=True)),
                ('estado', models.CharField(max_length=20)),
            ],
            options={'db_table': 'vivienda', 'managed': False},
        ),
        migrations.CreateModel(
            name='Residente',
            fields=[
                ('id_residente', models.AutoField(primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=80)),
                ('apellidos', models.CharField(max_length=80)),
                ('correo', models.EmailField(blank=True, max_length=120, null=True, unique=True)),
                ('telefono', models.CharField(max_length=20)),
                ('tipo_residente', models.CharField(max_length=20)),
                ('titular', models.CharField(max_length=2)),
                ('documento', models.CharField(max_length=20, unique=True)),
                ('vivienda', models.ForeignKey(db_column='id_vivienda', on_delete=django.db.models.deletion.DO_NOTHING, related_name='residentes', to='residentes.vivienda')),
            ],
            options={'db_table': 'residentes', 'managed': False},
        ),
    ]
