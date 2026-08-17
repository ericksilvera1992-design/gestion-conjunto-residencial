"""
Modelos del módulo de residentes.

Este archivo representa las tablas existentes de la base de datos
gestion_conjunto_residencial mediante el ORM de Django.
"""

from django.db import models


class Vivienda(models.Model):
    """
    Representa una vivienda del conjunto residencial.
    """

    id_vivienda = models.AutoField(
        primary_key=True
    )

    tipo_vivienda = models.CharField(
        max_length=20
    )

    torre = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )

    codigo_vivienda = models.CharField(
        max_length=20,
        unique=True
    )

    estado = models.CharField(
        max_length=20
    )

    class Meta:
        """
        Configuración del modelo Vivienda.
        """

        db_table = 'vivienda'
        managed = False

    def __str__(self):
        """
        Devuelve una representación legible de la vivienda.
        """
        return self.codigo_vivienda


class Residente(models.Model):
    """
    Representa un residente del conjunto residencial.
    """

    id_residente = models.AutoField(
        primary_key=True
    )

    nombres = models.CharField(
        max_length=80
    )

    apellidos = models.CharField(
        max_length=80
    )

    correo = models.EmailField(
        max_length=120,
        unique=True,
        null=True,
        blank=True
    )

    telefono = models.CharField(
        max_length=20
    )

    tipo_residente = models.CharField(
        max_length=20
    )

    titular = models.CharField(
        max_length=2
    )

    documento = models.CharField(
        max_length=20,
        unique=True
    )

    vivienda = models.ForeignKey(
        Vivienda,
        on_delete=models.DO_NOTHING,
        db_column='id_vivienda',
        related_name='residentes'
    )

    class Meta:
        """
        Configuración del modelo Residente.
        """

        db_table = 'residentes'
        managed = False

    def __str__(self):
        """
        Devuelve el nombre completo del residente.
        """
        return f'{self.nombres} {self.apellidos}'