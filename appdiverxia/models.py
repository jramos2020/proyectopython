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
    nomcli = models.CharField(max_length=45)
    apecli = models.CharField(max_length=45)
    feccli = models.DateField()
    dnicli = models.CharField(max_length=8)
    dircli = models.CharField(max_length=45)
    #telcli = models.CharField(max_length=8)
    celcli = models.CharField(max_length=9)
    corcli = models.EmailField()
    estcli = models.BooleanField()  # This field type is a guess.
    codusu = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='codusu')


class Destino(models.Model):
    #coddes = models.IntegerField(primary_key=True)
    nomdes = models.CharField(max_length=45)
    estdes = models.BooleanField()  # This field type is a guess.


class Detalleentrada(models.Model):
    nroent = models.ForeignKey('Entrada', models.DO_NOTHING, db_column='nroent')
    codpro = models.ForeignKey('Producto', models.DO_NOTHING, db_column='codpro')
    cantidad = models.IntegerField()


class Detallesalida(models.Model):
    cantidad = models.IntegerField()
    nrosal = models.ForeignKey('Salida', models.DO_NOTHING, db_column='nrosal')
    codpro = models.ForeignKey('Producto', models.DO_NOTHING, db_column='codpro')


class Detalleticket(models.Model):
    cantidad = models.IntegerField()
    nrotick = models.ForeignKey('Ticket', models.DO_NOTHING, db_column='nrotick')
    codpro = models.ForeignKey('Producto', models.DO_NOTHING, db_column='codpro')


class Empleado(models.Model):
    #codempleado = models.IntegerField(primary_key=True)
    nomemp = models.CharField(max_length=45)
    apeemp = models.CharField(max_length=45)
    dniemp = models.CharField(max_length=8)
    fechemp = models.DateField()
    #telemp = models.CharField(max_length=45)
    celemp = models.CharField(max_length=9)
    corremp = models.EmailField()
    estemp = models.BooleanField()  # This field type is a guess.
    codusu = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='codusu')


class Entrada(models.Model):
    #nroent = models.IntegerField(primary_key=True)
    codprov = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='codprov')
    codempleado = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='codempleado')
    fecha = models.DateTimeField()
    estent = models.BooleanField()  # This field type is a guess.

class Producto(models.Model):
    #codpro = models.IntegerField(primary_key=True)
    nompro = models.CharField(max_length=45)
    prepro = models.DecimalField(max_digits=7, decimal_places=2)
    stok = models.IntegerField()
    estpro = models.BooleanField()  # This field type is a guess.


class Proveedor(models.Model):
    #codprov = models.IntegerField(primary_key=True)
    nomprov = models.CharField(max_length=45)
    celprov = models.CharField(max_length=9)
    corrprov = models.EmailField()
    rucprov = models.CharField(max_length=11)
    estprov = models.BooleanField()


class Salida(models.Model):
    #nrosal = models.IntegerField(primary_key=True)
    coddes = models.ForeignKey('Destino', models.DO_NOTHING, db_column='coddes')
    codempleado = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='codempleado')
    techa = models.DateTimeField()
    estsal = models.BooleanField() # This field type is a guess.

class Ticket(models.Model):
    #nrotick = models.IntegerField(primary_key=True)
    codempleado = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='codempleado')
    codcli = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='codcli')
    fecha = models.DateField()
    est = models.BooleanField()  # This field type is a guess.
