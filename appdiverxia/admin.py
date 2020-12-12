from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from appdiverxia.forms import LoginFormulario
from appdiverxia.models import Usuario,MetodoPago,Cliente,Producto,Proveedor


class UsuarioAdmin(UserAdmin):
    add_form = LoginFormulario
    # form = CustomUserChangeForm
    model = Usuario
    list_display = ['email', 'username', ]


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(MetodoPago)
admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Producto)
