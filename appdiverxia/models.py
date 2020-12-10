from datetime import datetime
from enum import Enum

from django.db import models
from django.contrib.auth.models import AbstractUser


class Metodopago(models.Model):
    nombre = models.CharField(max_length=50)
    estado = models.BooleanField(default=1)

    def __str__(self):
        return "%s" % self.nombre


class Usuario(AbstractUser):
    address = models.CharField(max_length=100)


class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=150)
    fecha = models.DateField()
    dni = models.CharField(max_length=8)
    celular = models.CharField(max_length=9)
    correo = models.CharField(max_length=40, blank=True, null=True)
    estado = models.BooleanField(default=1)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING)

    def __str__(self):
        return "%s %s" % (self.nombre, self.apellido)


class Empleado(models.Model):
    EMPLEADO = 'EMPLEADO'
    REPARTIDOR = 'REPARTIDOR'
    YEAR_IN_SCHOOL_CHOICES = [
        (EMPLEADO, 'EMPLEADO'),
        (REPARTIDOR, 'REPARTIDOR'),
    ]

    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    tipo = models.CharField(max_length=255, choices=YEAR_IN_SCHOOL_CHOICES, default=EMPLEADO)
    dni = models.CharField(max_length=8)
    fecha = models.DateField()
    celular = models.CharField(max_length=9)
    correo = models.CharField(max_length=40)
    estado = models.BooleanField(default=1)  # This field type is a guess.
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    direccion = models.CharField(max_length=150)

    def __str__(self):
        return "%s %s (%s)" % (self.nombre, self.apellido, self.dni)


class Proveedor(models.Model):
    nombre = models.CharField(max_length=40)
    celular = models.CharField(max_length=9)
    correo = models.CharField(max_length=40)
    ruc = models.CharField(max_length=11)
    direccion = models.CharField(max_length=150)
    estado = models.BooleanField(default=1)  # This field type is a guess.

    def __str__(self):
        return "%s (%s)" % (self.nombre, self.ruc)


class Producto(models.Model):
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.IntegerField(blank=True, null=True)
    estado = models.BooleanField(default=1)  # This field type is a guess.

    def __str__(self):
        return "%s" % self.nombre




class Ticket(models.Model):
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)
    empleado = models.ForeignKey(Empleado, models.DO_NOTHING)
    fecha = models.DateTimeField(default=datetime.now())
    estado = models.BooleanField(default=1)
    detalle = models.ManyToManyField(Producto,through='TicketDetalle')


class TicketDetalle(models.Model):
    ticket = models.ForeignKey('Ticket',  on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    class Meta:
        unique_together = (('ticket', 'producto'),)


class Comprobantepago(models.Model):
    ticket = models.ForeignKey('Ticket', models.DO_NOTHING)
    empleado = models.ForeignKey('Empleado', models.DO_NOTHING)
    tipo = models.CharField(max_length=8)
    fecha = models.DateTimeField()
    estado = models.BooleanField(default=1)  # This field type is a guess.
    pago = models.ForeignKey('Metodopago', models.DO_NOTHING)


class Entrada(models.Model):
    proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING)
    empleado = models.ForeignKey(Empleado, models.DO_NOTHING)
    fecha = models.DateTimeField()
    estado = models.BooleanField(default=1)  # This field type is a guess.


class Detalleentrada(models.Model):
    entrada = models.OneToOneField('Entrada', models.DO_NOTHING)
    producto = models.ForeignKey('Producto', models.DO_NOTHING)
    cantidad = models.IntegerField()

    class Meta:
        unique_together = (('entrada', 'producto'),)


class Salida(models.Model):
    direccion = models.CharField(max_length=150)
    empleado = models.ForeignKey(Empleado, models.DO_NOTHING)
    fecha = models.DateTimeField()
    estado = models.BooleanField(default=1)  # This field type is a guess.


class Detallesalida(models.Model):
    salida = models.OneToOneField('Salida', models.DO_NOTHING)
    producto = models.ForeignKey('Producto', models.DO_NOTHING)
    cantidad = models.IntegerField()

    class Meta:
        unique_together = (('salida', 'producto'),)

# Create your models here.
