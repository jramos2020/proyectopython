from django.db import models
from django.contrib.auth.models import AbstractUser


class Persona(models.Model):
    codper = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.CharField(max_length=60)
    correo = models.EmailField()
    telefono = models.CharField(max_length=9)


class Usuario(AbstractUser):
    address = models.CharField(max_length=100)


# perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)

# Create your models here.

class Cliente(models.Model):
    #codcli = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    fecha = models.DateField()
    dni = models.CharField(max_length=8)
    direccion = models.CharField(max_length=45)
    celular = models.CharField(max_length=9)
    correo = models.EmailField()
    estado = models.BooleanField()  # This field type is a guess.
    usuario_id = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_id')

class Direccion(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.BooleanField()  # This field type is a guess.

class Detalleentrada(models.Model):
    nroent = models.ForeignKey('Entrada', models.DO_NOTHING, db_column='nroent')
    producto_id = models.ForeignKey('Producto', models.DO_NOTHING, db_column='producto_id')
    cantidad = models.IntegerField()


class Detallesalida(models.Model):
    cantidad = models.IntegerField()
    nrosal = models.ForeignKey('Salida', models.DO_NOTHING, db_column='nrosal')
    producto_id = models.ForeignKey('Producto', models.DO_NOTHING, db_column='producto_id')


class Detalleticket(models.Model):
    cantidad = models.IntegerField()
    ticket_id = models.ForeignKey('Ticket', models.DO_NOTHING, db_column='ticket_id')
    producto_id = models.ForeignKey('Producto', models.DO_NOTHING, db_column='producto_id')


class Empleado(models.Model):

    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    dni = models.CharField(max_length=8)
    fecha = models.DateField()
    celular = models.CharField(max_length=9)
    correo = models.EmailField()
    estado = models.BooleanField()  # This field type is a guess.
    usuario_id = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_id')
    direccion_id = models.ForeignKey('Direccion', models.DO_NOTHING, db_column='direccion_id')


class Entrada(models.Model):
    proveedor_id = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='proveedor_id')
    empleado_id = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='empleado_id')
    fecha = models.DateTimeField()
    estado = models.BooleanField()  # This field type is a guess.

class Producto(models.Model):
    nombre = models.CharField(max_length=45)
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.IntegerField()
    estado = models.BooleanField()  # This field type is a guess.


class Proveedor(models.Model):

    nombre = models.CharField(max_length=45)
    celular = models.CharField(max_length=9)
    correo = models.EmailField()
    ruc = models.CharField(max_length=11)
    estado = models.BooleanField()
    direccion_id = models.ForeignKey('Direccion', models.DO_NOTHING, db_column='direccion_id')

class Salida(models.Model):

    direccion_id = models.ForeignKey('Direccion', models.DO_NOTHING, db_column='direccion_id')
    empleado_id = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='empleado_id')
    fecha = models.DateTimeField()
    estado = models.BooleanField() # This field type is a guess.

class Ticket(models.Model):

    empleado_id = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='empleado_id')
    cliente_id = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='cliente_id')
    fecha = models.DateField()
    estado = models.BooleanField()  # This field type is a guess.

class MetodoPago(models.Model):
    tipopago = models.CharField(max_length=9)
    estado = models.BooleanField()  # This field type is a guess.

class Repartidor(models.Model):

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=8)
    celular = models.CharField(max_length=9)
    estado = models.BooleanField()

class ComprobantePago(models.Model):

    empleado_id = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='empleado_id')
    cliente_id = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='cliente_id')
    fecha = models.DateField()
    estado = models.BooleanField()  # This field type is a guess.


