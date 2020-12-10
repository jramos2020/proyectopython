from django.db import models
from django.contrib.auth.models import AbstractUser


class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=60)
    correo = models.EmailField()
    telefono = models.CharField(max_length=9)


class Usuario(AbstractUser):
    address = models.CharField(max_length=100)

    class Meta:
        db_table = 'auth_user'


class Cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha = models.DateField()
    dni = models.CharField(max_length=8)
    celular = models.CharField(max_length=9)
    correo = models.CharField(max_length=40, blank=True, null=True)
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    direccion = models.ForeignKey('Direccion', models.DO_NOTHING)


class Comprobantepago(models.Model):
    ticket = models.ForeignKey('Ticket', models.DO_NOTHING)
    empleado = models.ForeignKey('Empleado', models.DO_NOTHING)
    tipo = models.CharField(max_length=8)
    fecha = models.DateTimeField()
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.
    pago = models.ForeignKey('Metodopago', models.DO_NOTHING)
    repartidor = models.ForeignKey('Repartidor', models.DO_NOTHING)


class Detalleentrada(models.Model):
    entrada = models.OneToOneField('Entrada', models.DO_NOTHING, primary_key=True)
    producto = models.ForeignKey('Producto', models.DO_NOTHING)
    cantidad = models.IntegerField()

    class Meta:
        unique_together = (('entrada', 'producto'),)


class Detallesalida(models.Model):
    salida = models.OneToOneField('Salida', models.DO_NOTHING, primary_key=True)
    producto = models.ForeignKey('Producto', models.DO_NOTHING)
    cantidad = models.IntegerField()

    class Meta:
        unique_together = (('salida', 'producto'),)


class Detalleticket(models.Model):
    ticket = models.OneToOneField('Ticket', models.DO_NOTHING, primary_key=True)
    producto = models.ForeignKey('Producto', models.DO_NOTHING)
    cantidad = models.IntegerField()

    class Meta:
        unique_together = (('ticket', 'producto'),)


class Direccion(models.Model):
    nombre = models.CharField(max_length=40)
    estado = models.TextField()  # This field type is a guess.


class Empleado(models.Model):
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    dni = models.CharField(max_length=8)
    fecha = models.DateField()
    celular = models.CharField(max_length=9)
    correo = models.CharField(max_length=40)
    estado = models.TextField()  # This field type is a guess.
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    direccion = models.ForeignKey(Direccion, models.DO_NOTHING)


class Entrada(models.Model):
    proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING)
    empleado = models.ForeignKey(Empleado, models.DO_NOTHING)
    fecha = models.DateTimeField()
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.


class Metodopago(models.Model):
    tipopago = models.CharField(max_length=50)
    estado = models.TextField()  # This field type is a guess.


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.IntegerField(blank=True, null=True)
    estado = models.BooleanField()  # This field type is a guess.


class Proveedor(models.Model):
    nombre = models.CharField(max_length=40)
    celular = models.CharField(max_length=9)
    correo = models.CharField(max_length=40)
    ruc = models.CharField(max_length=11)
    estado = models.TextField()  # This field type is a guess.
    direccion = models.ForeignKey(Direccion, models.DO_NOTHING)


class Repartidor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=5)
    celular = models.CharField(max_length=9)
    estado = models.TextField()  # This field type is a guess.


class Salida(models.Model):
    direccion = models.ForeignKey(Direccion, models.DO_NOTHING)
    empleado = models.ForeignKey(Empleado, models.DO_NOTHING)
    fecha = models.DateTimeField()
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.


class Ticket(models.Model):
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)
    empleado = models.ForeignKey(Empleado, models.DO_NOTHING)
    fecha = models.DateTimeField()
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.

    # perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)

# Create your models here.
