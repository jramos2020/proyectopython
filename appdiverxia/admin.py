from django.contrib import admin

# Register your models here.

from appdiverxia.models import Usuario
from appdiverxia.models import Empleado
from appdiverxia.models import Cliente
from appdiverxia.models import Producto
from appdiverxia.models import Proveedor
from appdiverxia.models import Destino
from appdiverxia.models import Salida
from appdiverxia.models import Entrada
from appdiverxia.models import Ticket

from appdiverxia.models import Detalleentrada
from appdiverxia.models import Detallesalida
from appdiverxia.models import Detalleticket

from appdiverxia.models import Persona
from django.contrib.auth.admin import UserAdmin

admin.site.register(Usuario,UserAdmin)
admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Destino)
admin.site.register(Salida)
admin.site.register(Entrada)
admin.site.register(Ticket)

admin.site.register(Detalleentrada)
admin.site.register(Detallesalida)
admin.site.register(Detalleticket)

admin.site.register(Persona)