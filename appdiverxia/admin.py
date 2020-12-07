from django.contrib import admin

# Register your models here.

from appdiverxia.models import Usuario
from appdiverxia.models import Empleado
from appdiverxia.models import Cliente
from appdiverxia.models import Producto
from appdiverxia.models import Proveedor
from appdiverxia.models import Destino

from appdiverxia.models import Persona
from django.contrib.auth.admin import UserAdmin

admin.site.register(Usuario,UserAdmin)
admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Destino)

admin.site.register(Persona)