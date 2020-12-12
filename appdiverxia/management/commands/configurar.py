from django.core.management.base import BaseCommand, CommandError
import os
from appdiverxia.models import Opciones
from django.core.management import call_command

from django.contrib.auth import get_user_model
from appdiverxia.models import Usuario

class Command(BaseCommand):
    help = 'Insetar campos por defecto en la base de datos postinstalacion'
    """
    def add_arguments(self, parser):
        parser.add_argument('erase_file', nargs='+', type=str)
    """

    def handle(self, *args, **options):
        self.UserModel = get_user_model()
        call_command('reset_db',noinput=True)
        call_command('makemigrations', 'appdiverxia')
        call_command('migrate')
        try:
            objs = Usuario.objects.get(username='admin')
        except:
            user_data = {}
            user_data[self.UserModel.USERNAME_FIELD] = 'admin'
            user_data['email'] = 'admin@admin.com'
            user_data['password'] = 'password'
            database = 'default'
            self.UserModel._default_manager.db_manager(database).create_superuser(**user_data)

        objs = Opciones.objects.all()
        if len(objs) == 0:
            op = Opciones(moneda='S/.', valor_igv='18', nombre_negocio='Diverxia S.A.C',
                          mensaje_factura='Gracias por su preferencia')
            op.save()
