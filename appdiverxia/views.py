# renderiza las vistas al usuario
from django.shortcuts import render
# para redirigir a otras paginas
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
# el formulario de login
from .forms import *
# clase para crear vistas basadas en sub-clases
from django.views import View
# autentificacion de usuario e inicio de sesion
from django.contrib.auth import authenticate, login, logout
# verifica si el usuario esta logeado
from django.contrib.auth.mixins import LoginRequiredMixin

# modelos
from .models import *
# formularios dinamicos
from django.forms import formset_factory
# funciones personalizadas
from .funciones import *
# Mensajes de formulario
from django.contrib import messages
# Ejecuta un comando en la terminal externa
from django.core.management import call_command
# procesa archivos en .json
from django.core import serializers
# permite acceder de manera mas facil a los ficheros
from django.core.files.storage import FileSystemStorage
from django.urls import reverse


# Vistas endogenas.


# Interfaz de inicio de sesion----------------------------------------------------#
class Login(View):
    # Si el usuario ya envio el formulario por metodo post
    def post(self, request):
        # Crea una instancia del formulario y la llena con los datos:
        form = LoginFormulario(request.POST)
        # Revisa si es valido:
        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            usuario = form.cleaned_data['username']
            clave = form.cleaned_data['password']
            # Se verifica que el usuario y su clave existan
            logeado = authenticate(request, username=usuario, password=clave)
            if logeado is not None:
                login(request, logeado)
                # Si el login es correcto lo redirige al panel del sistema:
                return HttpResponseRedirect(reverse('appdiverxia:panel'))
            else:
                # De lo contrario lanzara el mismo formulario
                return render(request, 'appdiverxia/login.html', {'form': form})

    # Si se llega por GET crearemos un formulario en blanco
    def get(self, request):
        if request.user.is_authenticated == True:
            return HttpResponseRedirect(reverse('appdiverxia:panel'))

        form = LoginFormulario()
        # Envia al usuario el formulario para que lo llene
        return render(request, 'appdiverxia/login.html', {'form': form})


# Fin de vista---------------------------------------------------------------------#


# Panel de inicio y vista principal------------------------------------------------#
class Panel(LoginRequiredMixin, View):
    # De no estar logeado, el usuario sera redirigido a la pagina de Login
    # Las dos variables son la pagina a redirigir y el campo adicional, respectivamente
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        from datetime import date
        # Recupera los datos del usuario despues del login
        contexto = {'usuario': request.user.username,
                    'id_usuario': request.user.id,
                    'nombre': request.user.first_name,
                    'apellido': request.user.last_name,
                    'correo': request.user.email,
                    'fecha': date.today(),
                    'productosRegistrados': Producto.numeroRegistrados(),
                    'productosVendidos': DetalleFactura.productosVendidos(),
                    'clientesRegistrados': Cliente.numeroRegistrados(),
                    'usuariosRegistrados': Usuario.numeroRegistrados(),
                    'facturasEmitidas': Factura.numeroRegistrados(),
                    'ingresoTotal': Factura.ingresoTotal(),
                    'ultimasVentas': DetalleFactura.ultimasVentas(),
                    'administradores': Usuario.numeroUsuarios('administrador'),
                    'usuarios': Usuario.numeroUsuarios('usuario')

                    }

        return render(request, 'appdiverxia/panel.html', contexto)


# Fin de vista----------------------------------------------------------------------#


# Maneja la salida del usuario------------------------------------------------------#
class Salir(LoginRequiredMixin, View):
    # Sale de la sesion actual
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('appdiverxia:login'))


# Fin de vista----------------------------------------------------------------------#

# Muestra el perfil del usuario logeado actualmente---------------------------------#
class Perfil(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    # se accede al modo adecuado y se valida al usuario actual para ver si puede modificar al otro usuario-
    # -el cual es obtenido por la variable 'p'
    def get(self, request, modo, p):
        if modo == 'editar':
            perf = Usuario.objects.get(id=p)
            editandoSuperAdmin = False

            if p == 1:
                if request.user.nivel != 2:
                    messages.error(request,
                                   'No puede editar el perfil del administrador por no tener los permisos suficientes')
                    return HttpResponseRedirect(reverse('appdiverxia:perfil', args=('ver', p,)))
                editandoSuperAdmin = True
            else:
                if request.user.is_superuser != True:
                    messages.error(request, 'No puede cambiar el perfil por no tener los permisos suficientes')
                    return HttpResponseRedirect(reverse('appdiverxia:perfil', args=('ver', p,)))

                else:
                    if perf.is_superuser == True:
                        if request.user.nivel == 2:
                            pass

                        elif perf.id != request.user.id:
                            messages.error(request, 'No puedes cambiar el perfil de un usuario de tu mismo nivel')

                            return HttpResponseRedirect(reverse('appdiverxia:perfil', args=('ver', p,)))

            if editandoSuperAdmin:
                form = UsuarioFormulario()
                form.fields['level'].disabled = True
            else:
                form = UsuarioFormulario()

            # Me pregunto si habia una manera mas facil de hacer esto, solo necesitaba hacer que el formulario-
            # -apareciera lleno de una vez, pero arrojaba User already exists y no pasaba de form.is_valid()
            form['username'].field.widget.attrs['value'] = perf.username
            form['first_name'].field.widget.attrs['value'] = perf.first_name
            form['last_name'].field.widget.attrs['value'] = perf.last_name
            form['email'].field.widget.attrs['value'] = perf.email
            form['level'].field.widget.attrs['value'] = perf.nivel

            # Envia al usuario el formulario para que lo llene
            contexto = {'form': form, 'modo': request.session.get('perfilProcesado'), 'editar': 'perfil',
                        'nombreUsuario': perf.username}

            contexto = complementarContexto(contexto, request.user)
            return render(request, 'appdiverxia/perfil/perfil.html', contexto)


        elif modo == 'clave':
            perf = Usuario.objects.get(id=p)
            if p == 1:
                if request.user.nivel != 2:
                    messages.error(request,
                                   'No puede cambiar la clave del administrador por no tener los permisos suficientes')
                    return HttpResponseRedirect(reverse('appdiverxia:perfil', args=('ver', p,)))
            else:
                if request.user.is_superuser != True:
                    messages.error(request,
                                   'No puede cambiar la clave de este perfil por no tener los permisos suficientes')
                    return HttpResponseRedirect(reverse('appdiverxia:perfil', args=('ver', p,)))

                else:
                    if perf.is_superuser == True:
                        if request.user.nivel == 2:
                            pass

                        elif perf.id != request.user.id:
                            messages.error(request, 'No puedes cambiar la clave de un usuario de tu mismo nivel')
                            return HttpResponseRedirect(reverse('appdiverxia:perfil', args=('ver', p,)))

            form = ClaveFormulario(request.POST)
            contexto = {'form': form, 'modo': request.session.get('perfilProcesado'),
                        'editar': 'clave', 'nombreUsuario': perf.username}

            contexto = complementarContexto(contexto, request.user)
            return render(request, 'appdiverxia/perfil/perfil.html', contexto)

        elif modo == 'ver':
            perf = Usuario.objects.get(id=p)
            contexto = {'perfil': perf}
            contexto = complementarContexto(contexto, request.user)

            return render(request, 'appdiverxia/perfil/verPerfil.html', contexto)

    def post(self, request, modo, p):
        if modo == 'editar':
            # Crea una instancia del formulario y la llena con los datos:
            form = UsuarioFormulario(request.POST)
            # Revisa si es valido:

            if form.is_valid():
                perf = Usuario.objects.get(id=p)
                # Procesa y asigna los datos con form.cleaned_data como se requiere
                if p != 1:
                    level = form.cleaned_data['level']
                    perf.nivel = level
                    perf.is_superuser = level

                username = form.cleaned_data['username']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']

                perf.username = username
                perf.first_name = first_name
                perf.last_name = last_name
                perf.email = email

                perf.save()

                form = UsuarioFormulario()
                messages.success(request, 'Actualizado exitosamente el perfil de ID %s.' % p)
                request.session['perfilProcesado'] = True
                return HttpResponseRedirect(reverse("appdiverxia:perfil",args=('ver',perf.id,)))
            else:
                # De lo contrario lanzara el mismo formulario
                return render(request, 'appdiverxia/perfil/perfil.html', {'form': form})

        elif modo == 'clave':
            form = ClaveFormulario(request.POST)

            if form.is_valid():
                error = 0
                clave_nueva = form.cleaned_data['clave_nueva']
                repetir_clave = form.cleaned_data['repetir_clave']
                # clave = form.cleaned_data['clave']

                # Comentare estas lineas de abajo para deshacerme de la necesidad
                #   de obligar a que el usuario coloque la clave nuevamente
                # correcto = authenticate(username=request.user.username , password=clave)

                # if correcto is not None:
                # if clave_nueva != clave:
                # pass
                # else:
                # error = 1
                # messages.error(request,"La clave nueva no puede ser identica a la actual")

                usuario = Usuario.objects.get(id=p)

                if clave_nueva == repetir_clave:
                    pass
                else:
                    error = 1
                    messages.error(request, "La clave nueva y su repeticion tienen que coincidir")

                # else:
                # error = 1
                # messages.error(request,"La clave de acceso actual que ha insertado es incorrecta")

                if (error == 0):
                    messages.success(request, 'La clave se ha cambiado correctamente!')
                    usuario.set_password(clave_nueva)
                    usuario.save()
                    return HttpResponseRedirect(reverse("appdiverxia:login"))

                else:
                    return HttpResponseRedirect(reverse("appdiverxia:perfil", args=('clave', p,)))


# ----------------------------------------------------------------------------------#


# Elimina usuarios, productos, clientes o proveedores----------------------------
class Eliminar(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request, modo, p):

        if modo == 'producto':
            prod = Producto.objects.get(id=p)
            prod.delete()
            messages.success(request, 'Producto de ID %s borrado exitosamente.' % p)
            return HttpResponseRedirect(reverse("appdiverxia:listarProductos"))

        elif modo == 'cliente':
            cliente = Cliente.objects.get(id=p)
            cliente.delete()
            messages.success(request, 'Cliente de ID %s borrado exitosamente.' % p)
            return HttpResponseRedirect(reverse("appdiverxia:listarClientes"))


        elif modo == 'proveedor':
            proveedor = Proveedor.objects.get(id=p)
            proveedor.delete()
            messages.success(request, 'Proveedor de ID %s borrado exitosamente.' % p)
            return HttpResponseRedirect(reverse("appdiverxia:listarProveedores"))

        elif modo == 'usuario':
            if request.user.is_superuser == False:
                messages.error(request, 'No tienes permisos suficientes para borrar usuarios')
                return HttpResponseRedirect(reverse('appdiverxia:listarUsuarios'))

            elif p == 1:
                messages.error(request, 'No puedes eliminar al super-administrador.')
                return HttpResponseRedirect(reverse('appdiverxia:listarUsuarios'))

            elif request.user.id == p:
                messages.error(request, 'No puedes eliminar tu propio usuario.')
                return HttpResponseRedirect(reverse('appdiverxia:listarUsuarios'))

            else:
                usuario = Usuario.objects.get(id=p)
                usuario.delete()
                messages.success(request, 'Usuario de ID %s borrado exitosamente.' % p)
                return HttpResponseRedirect(reverse("appdiverxia:listarUsuarios"))


# Fin de vista-------------------------------------------------------------------


class ListarMetodosPago(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        metodospagos = MetodoPago.objects.all()

        contexto = {'tabla': metodospagos}

        contexto = complementarContexto(contexto, request.user)

        return render(request, 'appdiverxia/metodospago/listar.html', contexto)


class AgregarMetodosPago(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request):
        # Crea una instancia del formulario y la llena con los datos:
        form = MetodoPagoFormulario(request.POST)
        # Revisa si es valido:

        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            estado = form.cleaned_data['estado']

            metodopago = MetodoPago(nombre=nombre, descripcion=descripcion, estado=estado)
            metodopago.save()
            form = MetodoPagoFormulario()

            messages.success(request, 'Ingresado exitosamente bajo la ID %s.' % metodopago.id)
            request.session['metodoPagoProcesado'] = 'agregado'
            return HttpResponseRedirect(reverse("appdiverxia:metodospago.agregar"))
        else:
            # De lo contrario lanzara el mismo formulario
            return render(request, 'appdiverxia/metodospago/agregar.html', {'form': form})

    def get(self, request):
        form = MetodoPagoFormulario()
        # Envia al usuario el formulario para que lo llene
        contexto = {'form': form, 'modo': request.session.get('metodoPagoProcesado')}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/metodospago/agregar.html', contexto)


class EditarMetodosPago(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request, p):
        # Crea una instancia del formulario y la llena con los datos:
        form = MetodoPagoFormulario(request.POST)
        # Revisa si es valido:
        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            estado = form.cleaned_data['estado']

            metodopago = MetodoPago.objects.get(id=p)
            metodopago.nombre = nombre
            metodopago.descripcion = descripcion
            metodopago.estado = estado
            metodopago.save()
            form = MetodoPagoFormulario(instance=metodopago)
            messages.success(request, 'Actualizado exitosamente el metodode pago de ID %s.' % p)
            request.session['metodoPagoProcesado'] = 'editado'
            return HttpResponseRedirect(reverse('appdiverxia:metodospago.editar', args=(p,)))
        else:
            # De lo contrario lanzara el mismo formulario
            return render(request, 'appdiverxia/metodospago/agregar.html', {'form': form})

    def get(self, request, p):
        prod = MetodoPago.objects.get(id=p)
        form = MetodoPagoFormulario(instance=prod)
        # Envia al usuario el formulario para que lo llene
        contexto = {'form': form, 'modo': request.session.get('metodoPagoProcesado'), 'editar': True}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/metodospago/agregar.html', contexto)



# Muestra una lista de 10 productos por pagina----------------------------------------#
class ListarProductos(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        from django.db import models

        # Lista de productos de la BDD
        productos = Producto.objects.all()

        contexto = {'tabla': productos}

        contexto = complementarContexto(contexto, request.user)

        return render(request, 'appdiverxia/producto/listarProductos.html', contexto)


# Fin de vista-------------------------------------------------------------------------#


# Maneja y visualiza un formulario--------------------------------------------------#
class AgregarProducto(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request):
        # Crea una instancia del formulario y la llena con los datos:
        form = ProductoFormulario(request.POST)
        # Revisa si es valido:
        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            descripcion = form.cleaned_data['descripcion']
            precio = form.cleaned_data['precio']
            categoria = '1'  # form.cleaned_data['categoria']
            tiene_igv = form.cleaned_data['tiene_igv']
            disponible = 0

            prod = Producto(descripcion=descripcion, precio=precio, categoria=categoria, tiene_igv=tiene_igv,
                            disponible=disponible)
            prod.save()

            form = ProductoFormulario()
            messages.success(request, 'Ingresado exitosamente bajo la ID %s.' % prod.id)
            request.session['productoProcesado'] = 'agregado'
            return HttpResponseRedirect(reverse("appdiverxia:agregarProducto"))
        else:
            # De lo contrario lanzara el mismo formulario
            return render(request, 'appdiverxia/producto/agregarProducto.html', {'form': form})

    # Si se llega por GET crearemos un formulario en blanco
    def get(self, request):
        form = ProductoFormulario()
        # Envia al usuario el formulario para que lo llene
        contexto = {'form': form, 'modo': request.session.get('productoProcesado')}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/producto/agregarProducto.html', contexto)


# Fin de vista------------------------------------------------------------------------#


# Formulario simple que procesa un script para importar los productos-----------------#
class ImportarProductos(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request):
        form = ImportarProductosFormulario(request.POST)
        if form.is_valid():
            request.session['productosImportados'] = True
            return HttpResponseRedirect(reverse("appdiverxia:importarProductos"))

    def get(self, request):
        form = ImportarProductosFormulario()

        if request.session.get('productosImportados') == True:
            importado = request.session.get('productoImportados')
            contexto = {'form': form, 'productosImportados': importado}
            request.session['productosImportados'] = False

        else:
            contexto = {'form': form}
            contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/producto/importarProductos.html', contexto)


# Fin de vista-------------------------------------------------------------------------#


# Formulario simple que crea un archivo y respalda los productos-----------------------#
class ExportarProductos(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request):
        form = ExportarProductosFormulario(request.POST)
        if form.is_valid():
            request.session['productosExportados'] = True

            # Se obtienen las entradas de producto en formato JSON
            data = serializers.serialize("json", Producto.objects.all())
            fs = FileSystemStorage('appdiverxia/tmp/')

            # Se utiliza la variable fs para acceder a la carpeta con mas facilidad
            with fs.open("productos.json", "w") as out:
                out.write(data)
                out.close()

            with fs.open("productos.json", "r") as out:
                response = HttpResponse(out.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'attachment; filename="productos.json"'
                out.close()
                # ------------------------------------------------------------
            return response

    def get(self, request):
        form = ExportarProductosFormulario()

        if request.session.get('productosExportados') == True:
            exportado = request.session.get('productoExportados')
            contexto = {'form': form, 'productosExportados': exportado}
            request.session['productosExportados'] = False

        else:
            contexto = {'form': form}
            contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/producto/exportarProductos.html', contexto)


# Fin de vista-------------------------------------------------------------------------#


# Muestra el formulario de un producto especifico para editarlo----------------------------------#
class EditarProducto(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request, p):
        # Crea una instancia del formulario y la llena con los datos:
        form = ProductoFormulario(request.POST)
        # Revisa si es valido:
        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            descripcion = form.cleaned_data['descripcion']
            precio = form.cleaned_data['precio']
            categoria = form.cleaned_data['categoria']
            tiene_igv = form.cleaned_data['tiene_igv']

            prod = Producto.objects.get(id=p)
            prod.descripcion = descripcion
            prod.precio = precio
            prod.categoria = categoria
            prod.tiene_igv = tiene_igv
            prod.save()
            form = ProductoFormulario(instance=prod)
            messages.success(request, 'Actualizado exitosamente el producto de ID %s.' % p)
            request.session['productoProcesado'] = 'editado'
            return HttpResponseRedirect(reverse("appdiverxia:editarProducto", args=(prod.id,)))
        else:
            # De lo contrario lanzara el mismo formulario
            return render(request, 'appdiverxia/producto/agregarProducto.html', {'form': form})

    def get(self, request, p):
        prod = Producto.objects.get(id=p)
        form = ProductoFormulario(instance=prod)
        # Envia al usuario el formulario para que lo llene
        contexto = {'form': form, 'modo': request.session.get('productoProcesado'), 'editar': True}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/producto/agregarProducto.html', contexto)


# Fin de vista------------------------------------------------------------------------------------#


# Crea una lista de los clientes, 10 por pagina----------------------------------------#
class ListarClientes(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        from django.db import models
        # Saca una lista de todos los clientes de la BDD
        clientes = Cliente.objects.all()
        contexto = {'tabla': clientes}
        contexto = complementarContexto(contexto, request.user)

        return render(request, 'appdiverxia/cliente/listarClientes.html', contexto)


# Fin de vista--------------------------------------------------------------------------#


# Crea y procesa un formulario para agregar a un cliente---------------------------------#
class AgregarCliente(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request):
        # Crea una instancia del formulario y la llena con los datos:
        form = ClienteFormulario(request.POST)
        # Revisa si es valido:

        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere

            documento_tipo = form.cleaned_data['tipoDocumento']
            documento = form.cleaned_data['documento']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            direccion = form.cleaned_data['direccion']
            nacimiento = form.cleaned_data['nacimiento']
            telefono = form.cleaned_data['telefono']
            correo = form.cleaned_data['correo']

            cliente = Cliente(documento_tipo=documento_tipo, documento=documento, nombre=nombre, apellido=apellido,
                              direccion=direccion, nacimiento=nacimiento, telefono=telefono,
                              correo=correo)
            cliente.save()
            form = ClienteFormulario()

            messages.success(request, 'Ingresado exitosamente bajo la ID %s.' % cliente.id)
            request.session['clienteProcesado'] = 'agregado'
            return HttpResponseRedirect(reverse("appdiverxia:agregarCliente"))
        else:
            # De lo contrario lanzara el mismo formulario
            return render(request, 'appdiverxia/cliente/agregarCliente.html', {'form': form})

    def get(self, request):
        form = ClienteFormulario()
        # Envia al usuario el formulario para que lo llene
        contexto = {'form': form, 'modo': request.session.get('clienteProcesado')}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/cliente/agregarCliente.html', contexto)


# Fin de vista-----------------------------------------------------------------------------#


# Formulario simple que procesa un script para importar los clientes-----------------#
class ImportarClientes(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request):
        form = ImportarClientesFormulario(request.POST)
        if form.is_valid():
            request.session['clientesImportados'] = True
            return HttpResponseRedirect(reverse("appdiverxia:importarClientes"))

    def get(self, request):
        form = ImportarClientesFormulario()

        if request.session.get('clientesImportados') == True:
            importado = request.session.get('clientesImportados')
            contexto = {'form': form, 'clientesImportados': importado}
            request.session['clientesImportados'] = False

        else:
            contexto = {'form': form}
            contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/cliente/importarClientes.html', contexto)


# Fin de vista-------------------------------------------------------------------------#


# Formulario simple que crea un archivo y respalda los clientes-----------------------#
class ExportarClientes(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request):
        form = ExportarClientesFormulario(request.POST)
        if form.is_valid():
            request.session['clientesExportados'] = True

            # Se obtienen las entradas de producto en formato JSON
            data = serializers.serialize("json", Cliente.objects.all())
            fs = FileSystemStorage('appdiverxia/tmp/')

            # Se utiliza la variable fs para acceder a la carpeta con mas facilidad
            with fs.open("clientes.json", "w") as out:
                out.write(data)
                out.close()

            with fs.open("clientes.json", "r") as out:
                response = HttpResponse(out.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'attachment; filename="clientes.json"'
                out.close()
                # ------------------------------------------------------------
            return response

    def get(self, request):
        form = ExportarClientesFormulario()

        if request.session.get('clientesExportados') == True:
            exportado = request.session.get('clientesExportados')
            contexto = {'form': form, 'clientesExportados': exportado}
            request.session['clientesExportados'] = False

        else:
            contexto = {'form': form}
            contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/cliente/exportarClientes.html', contexto)


# Fin de vista-------------------------------------------------------------------------#


# Muestra el mismo formulario del cliente pero con los datos a editar----------------------#
class EditarCliente(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request, p):
        # Crea una instancia del formulario y la llena con los datos:
        cliente = Cliente.objects.get(id=p)
        form = ClienteFormulario(request.POST, instance=cliente)
        # Revisa si es valido:

        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            documento_tipo = form.cleaned_data['tipoDocumento']
            documento = form.cleaned_data['documento']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            direccion = form.cleaned_data['direccion']
            nacimiento = form.cleaned_data['nacimiento']
            telefono = form.cleaned_data['telefono']
            correo = form.cleaned_data['correo']

            cliente.documento_tipo = documento_tipo
            cliente.documento = documento
            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.direccion = direccion
            cliente.nacimiento = nacimiento
            cliente.telefono = telefono
            cliente.correo = correo
            cliente.save()
            form = ClienteFormulario(instance=cliente)

            messages.success(request, 'Actualizado exitosamente el cliente de ID %s.' % p)
            request.session['clienteProcesado'] = 'editado'
            return HttpResponseRedirect(reverse("appdiverxia:editarCliente", args=(cliente.id,)))
        else:
            # De lo contrario lanzara el mismo formulario
            return render(request, 'appdiverxia/cliente/agregarCliente.html', {'form': form})

    def get(self, request, p):
        cliente = Cliente.objects.get(id=p)
        form = ClienteFormulario(instance=cliente)
        # Envia al usuario el formulario para que lo llene
        contexto = {'form': form, 'modo': request.session.get('clienteProcesado'), 'editar': True}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/cliente/agregarCliente.html', contexto)


# Fin de vista--------------------------------------------------------------------------------#


# Emite la primera parte de la factura------------------------------#
class EmitirFactura(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request):
        # Crea una instancia del formulario y la llena con los datos:
        documentos = Cliente.documentosRegistradas()
        form = EmitirFacturaFormulario(request.POST, documentos=documentos)
        # Revisa si es valido:
        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            request.session['form_details'] = form.cleaned_data['productos']
            request.session['id_client'] = form.cleaned_data['cliente']
            request.session['id_metodopago'] = form.cleaned_data['metodopago'].id
            return HttpResponseRedirect(reverse('appdiverxia:detallesDeFactura'))
        else:
            # De lo contrario lanzara el mismo formulario
            return render(request, 'appdiverxia/factura/emitirFactura.html', {'form': form})

    def get(self, request):
        documentos = Cliente.documentosRegistradas()
        form = EmitirFacturaFormulario(documentos=documentos)
        contexto = {'form': form}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/factura/emitirFactura.html', contexto)


# Fin de vista---------------------------------------------------------------------------------#


# Muestra y procesa los detalles de cada producto de la factura--------------------------------#
class DetallesFactura(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        documento = request.session.get('id_client')
        productos = request.session.get('form_details')
        FacturaFormulario = formset_factory(DetallesFacturaFormulario, extra=productos)
        formset = FacturaFormulario()
        contexto = {'formset': formset}
        contexto = complementarContexto(contexto, request.user)

        return render(request, 'appdiverxia/factura/detallesFactura.html', contexto)

    def post(self, request):
        metodopago_id = request.session.get('id_metodopago')
        documento = request.session.get('id_client')
        productos = request.session.get('form_details')

        FacturaFormulario = formset_factory(DetallesFacturaFormulario, extra=productos)

        inicial = {
            'descripcion': '',
            'cantidad': 0,
            'subtotal': 0,
        }

        data = {
            'form-TOTAL_FORMS': productos,
            'form-INITIAL_FORMS': 0,
            'form-MAX_NUM_FORMS': '',
        }

        formset = FacturaFormulario(request.POST, data)

        if formset.is_valid():

            id_producto = []
            cantidad = []
            subtotal = []
            total_general = []
            sub_monto = 0
            monto_general = 0

            for form in formset:
                prodId = form.cleaned_data['descripcion'].id
                desc = form.cleaned_data['descripcion'].descripcion
                cant = form.cleaned_data['cantidad']
                sub = form.cleaned_data['valor_subtotal']
                id_producto.append(prodId)  # esta funcion, a estas alturas, es innecesaria porque ya tienes la id
                cantidad.append(cant)
                subtotal.append(sub)

            # Ingresa la factura
            # --Saca el sub-monto
            for index in subtotal:
                sub_monto += index

            # --Saca el monto general
            for index, element in enumerate(subtotal):
                if productoTieneIgv(id_producto[index]):
                    nuevoPrecio = sacarIgv(element)
                    monto_general += nuevoPrecio
                    total_general.append(nuevoPrecio)
                else:
                    monto_general += element
                    total_general.append(element)

            from datetime import date

            cliente = Cliente.objects.get(documento=documento)
            igv = igvActual('objeto')
            factura = Factura(cliente=cliente, fecha=date.today(), sub_monto=sub_monto, monto_general=monto_general,
                              igv=igv,metodopago_id=metodopago_id)

            factura.save()
            id_factura = factura

            for indice, elemento in enumerate(id_producto):
                objetoProducto = obtenerProducto(elemento)
                cantidadDetalle = cantidad[indice]
                subDetalle = subtotal[indice]
                totalDetalle = total_general[indice]

                detalleFactura = DetalleFactura(id_factura=id_factura, id_producto=objetoProducto,
                                                cantidad=cantidadDetalle
                                                , sub_total=subDetalle, total=totalDetalle)

                objetoProducto.disponible -= cantidadDetalle
                objetoProducto.save()

                detalleFactura.save()

            messages.success(request, 'Factura de ID %s insertada exitosamente.' % id_factura.id)
            return HttpResponseRedirect(reverse("appdiverxia:emitirFactura"))


# Fin de vista-----------------------------------------------------------------------------------#


# Muestra y procesa los detalles de cada producto de la factura--------------------------------#
class ListarFacturas(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        # Lista de productos de la BDD
        facturas = Factura.objects.all()
        # Crea el paginador

        contexto = {'tabla': facturas}
        contexto = complementarContexto(contexto, request.user)

        return render(request, 'appdiverxia/factura/listarFacturas.html', contexto)


# Fin de vista---------------------------------------------------------------------------------------#


# Muestra los detalles individuales de una factura------------------------------------------------#
class VerFactura(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request, p):
        factura = Factura.objects.get(id=p)
        detalles = DetalleFactura.objects.filter(id_factura_id=p)
        contexto = {'factura': factura, 'detalles': detalles}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/factura/verFactura.html', contexto)


# Fin de vista--------------------------------------------------------------------------------------#


# Genera la factura en CSV--------------------------------------------------------------------------#
class GenerarFactura(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request, p):
        import csv

        factura = Factura.objects.get(id=p)
        detalles = DetalleFactura.objects.filter(id_factura_id=p)

        nombre_factura = "factura_%s.csv" % (factura.id)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s"' % nombre_factura
        writer = csv.writer(response)

        writer.writerow(['Producto', 'Cantidad', 'Sub-total', 'Total',
                         'Porcentaje IGV utilizado: %s' % (factura.igv.valor_igv)])

        for producto in detalles:
            writer.writerow([producto.id_producto.descripcion, producto.cantidad, producto.sub_total, producto.total])

        writer.writerow(['Total general:', '', '', factura.monto_general])

        return response

        # Fin de vista--------------------------------------------------------------------------------------#


# Genera la factura en PDF--------------------------------------------------------------------------#
class GenerarFacturaPDF(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request, p):
        import io
        from reportlab.pdfgen import canvas
        import datetime

        factura = Factura.objects.get(id=p)
        general = Opciones.objects.get(id=1)
        detalles = DetalleFactura.objects.filter(id_factura_id=p)
        doctipo = None
        if factura.cliente.documento_tipo == 1:
            doctipo = 'DNI'
        else:
            doctipo = 'RUC'
        data = {
            'fecha': factura.fecha,
            'monto_general': factura.monto_general,
            'nombre_cliente': factura.cliente.nombre + " " + factura.cliente.apellido,
            'documento_cliente': factura.cliente.documento,
            'documento_tipo': doctipo,
            'id_reporte': factura.id,
            'igv': factura.igv.valor_igv,
            'detalles': detalles,
            'modo': 'factura',
            'general': general
        }

        nombre_factura = "factura_%s.pdf" % (factura.id)

        pdf = render_to_pdf('appdiverxia/PDF/prueba.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % nombre_factura

        return response

        # Fin de vista--------------------------------------------------------------------------------------#


# Crea una lista de los clientes, 10 por pagina----------------------------------------#
class ListarProveedores(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        from django.db import models
        # Saca una lista de todos los clientes de la BDD
        proveedores = Proveedor.objects.all()
        contexto = {'tabla': proveedores}
        contexto = complementarContexto(contexto, request.user)

        return render(request, 'appdiverxia/proveedor/listarProveedores.html', contexto)


# Fin de vista--------------------------------------------------------------------------#


# Crea y procesa un formulario para agregar a un proveedor---------------------------------#
class AgregarProveedor(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request):
        # Crea una instancia del formulario y la llena con los datos:
        form = ProveedorFormulario(request.POST)
        # Revisa si es valido:

        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere

            documento_tipo = form.cleaned_data['tipoDocumento']
            documento = form.cleaned_data['documento']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            direccion = form.cleaned_data['direccion']
            nacimiento = form.cleaned_data['nacimiento']
            telefono = form.cleaned_data['telefono']
            correo = form.cleaned_data['correo']

            proveedor = Proveedor(documento_tipo=documento_tipo, documento=documento, nombre=nombre, apellido=apellido,
                                  direccion=direccion, nacimiento=nacimiento, telefono=telefono,
                                  correo=correo)
            proveedor.save()
            form = ProveedorFormulario()

            messages.success(request, 'Ingresado exitosamente bajo la ID %s.' % proveedor.id)
            request.session['proveedorProcesado'] = 'agregado'
            return HttpResponseRedirect(reverse("appdiverxia:agregarProveedor"))
        else:
            # De lo contrario lanzara el mismo formulario
            return render(request, 'appdiverxia/proveedor/agregarProveedor.html', {'form': form})

    def get(self, request):
        form = ProveedorFormulario()
        # Envia al usuario el formulario para que lo llene
        contexto = {'form': form, 'modo': request.session.get('proveedorProcesado')}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/proveedor/agregarProveedor.html', contexto)


# Fin de vista-----------------------------------------------------------------------------#

# Formulario simple que procesa un script para importar los proveedores-----------------#
class ImportarProveedores(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request):
        form = ImportarClientesFormulario(request.POST)
        if form.is_valid():
            request.session['clientesImportados'] = True
            return HttpResponseRedirect(reverse("appdiverxia:importarClientes"))

    def get(self, request):
        form = ImportarClientesFormulario()

        if request.session.get('clientesImportados') == True:
            importado = request.session.get('clientesImportados')
            contexto = {'form': form, 'clientesImportados': importado}
            request.session['clientesImportados'] = False

        else:
            contexto = {'form': form}
            contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/importarClientes.html', contexto)


# Fin de vista-------------------------------------------------------------------------#


# Formulario simple que crea un archivo y respalda los proveedores-----------------------#
class ExportarProveedores(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request):
        form = ExportarClientesFormulario(request.POST)
        if form.is_valid():
            request.session['clientesExportados'] = True

            # Se obtienen las entradas de producto en formato JSON
            data = serializers.serialize("json", Cliente.objects.all())
            fs = FileSystemStorage('appdiverxia/tmp/')

            # Se utiliza la variable fs para acceder a la carpeta con mas facilidad
            with fs.open("clientes.json", "w") as out:
                out.write(data)
                out.close()

            with fs.open("clientes.json", "r") as out:
                response = HttpResponse(out.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'attachment; filename="clientes.json"'
                out.close()
                # ------------------------------------------------------------
            return response

    def get(self, request):
        form = ExportarClientesFormulario()

        if request.session.get('clientesExportados') == True:
            exportado = request.session.get('clientesExportados')
            contexto = {'form': form, 'clientesExportados': exportado}
            request.session['clientesExportados'] = False

        else:
            contexto = {'form': form}
            contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/exportarClientes.html', contexto)


# Fin de vista-------------------------------------------------------------------------#


# Muestra el mismo formulario del cliente pero con los datos a editar----------------------#
class EditarProveedor(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def post(self, request, p):
        # Crea una instancia del formulario y la llena con los datos:
        proveedor = Proveedor.objects.get(id=p)
        form = ProveedorFormulario(request.POST, instance=proveedor)
        # Revisa si es valido:

        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            documento_tipo = form.cleaned_data['tipoDocumento']
            documento = form.cleaned_data['documento']
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            direccion = form.cleaned_data['direccion']
            nacimiento = form.cleaned_data['nacimiento']
            telefono = form.cleaned_data['telefono']
            correo = form.cleaned_data['correo']

            proveedor.documento_tipo = documento_tipo
            proveedor.documento = documento
            proveedor.nombre = nombre
            proveedor.apellido = apellido
            proveedor.direccion = direccion
            proveedor.nacimiento = nacimiento
            proveedor.telefono = telefono
            proveedor.correo = correo
            proveedor.save()
            form = ProveedorFormulario(instance=proveedor)

            messages.success(request, 'Actualizado exitosamente el proveedor de ID %s.' % p)
            request.session['proveedorProcesado'] = 'editado'
            return HttpResponseRedirect(reverse("appdiverxia/editarProveedor", args=(proveedor.id,)))
        else:
            # De lo contrario lanzara el mismo formulario
            return render(request, 'appdiverxia/proveedor/agregarProveedor.html', {'form': form})

    def get(self, request, p):
        proveedor = Proveedor.objects.get(id=p)
        form = ProveedorFormulario(instance=proveedor)
        # Envia al usuario el formulario para que lo llene
        contexto = {'form': form, 'modo': request.session.get('proveedorProcesado'), 'editar': True}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/proveedor/agregarProveedor.html', contexto)


# Fin de vista--------------------------------------------------------------------------------#


# Agrega un pedido-----------------------------------------------------------------------------------#
class AgregarPedido(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        documentos = Proveedor.documentosRegistradas()
        form = EmitirPedidoFormulario(documentos=documentos)
        contexto = {'form': form}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/pedido/emitirPedido.html', contexto)

    def post(self, request):
        # Crea una instancia del formulario y la llena con los datos:
        documentos = Proveedor.documentosRegistradas()
        form = EmitirPedidoFormulario(request.POST, documentos=documentos)
        # Revisa si es valido:
        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            request.session['form_details'] = form.cleaned_data['productos']
            request.session['id_proveedor'] = form.cleaned_data['proveedor']
            return HttpResponseRedirect(reverse('appdiverxia:detallesPedido'))
        else:
            # De lo contrario lanzara el mismo formulario
            return render(request, 'appdiverxia/pedido/emitirPedido.html', {'form': form})


# --------------------------------------------------------------------------------------------------#


# Lista todos los pedidos---------------------------------------------------------------------------#
class ListarPedidos(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        from django.db import models
        # Saca una lista de todos los clientes de la BDD
        pedidos = Pedido.objects.all()
        contexto = {'tabla': pedidos}
        contexto = complementarContexto(contexto, request.user)

        return render(request, 'appdiverxia/pedido/listarPedidos.html', contexto)


# ------------------------------------------------------------------------------------------------#


# Muestra y procesa los detalles de cada producto de la factura--------------------------------#
class DetallesPedido(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        documento = request.session.get('id_proveedor')
        productos = request.session.get('form_details')
        PedidoFormulario = formset_factory(DetallesPedidoFormulario, extra=productos)
        formset = PedidoFormulario()
        contexto = {'formset': formset}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/pedido/detallesPedido.html', contexto)

    def post(self, request):
        documento = request.session.get('id_proveedor')
        productos = request.session.get('form_details')

        PedidoFormulario = formset_factory(DetallesPedidoFormulario, extra=productos)

        inicial = {
            'descripcion': '',
            'cantidad': 0,
            'subtotal': 0,
        }

        data = {
            'form-TOTAL_FORMS': productos,
            'form-INITIAL_FORMS': 0,
            'form-MAX_NUM_FORMS': '',
        }

        formset = PedidoFormulario(request.POST, data)

        if formset.is_valid():

            id_producto = []
            cantidad = []
            subtotal = []
            total_general = []
            sub_monto = 0
            monto_general = 0

            for form in formset:
                idProd = form.cleaned_data['descripcion'].id
                desc = form.cleaned_data['descripcion'].descripcion
                cant = form.cleaned_data['cantidad']
                sub = form.cleaned_data['valor_subtotal']

                id_producto.append(idProd)  # esta funcion, a estas alturas, es innecesaria porque ya tienes la id
                #id_producto.append(obtenerIdProducto(desc))  # esta funcion, a estas alturas, es innecesaria porque ya tienes la id
                cantidad.append(cant)
                subtotal.append(sub)

                # Ingresa la factura
            # --Saca el sub-monto
            for index in subtotal:
                sub_monto += index

            # --Saca el monto general
            for index, element in enumerate(subtotal):
                if productoTieneIgv(id_producto[index]):
                    nuevoPrecio = sacarIgv(element)
                    monto_general += nuevoPrecio
                    total_general.append(nuevoPrecio)
                else:
                    monto_general += element
                    total_general.append(element)

            from datetime import date

            proveedor = Proveedor.objects.get(documento=documento)
            igv = igvActual('objeto')
            presente = False
            pedido = Pedido(proveedor=proveedor, fecha=date.today(), sub_monto=sub_monto, monto_general=monto_general,
                            igv=igv,
                            presente=presente)

            pedido.save()
            id_pedido = pedido

            for indice, elemento in enumerate(id_producto):
                objetoProducto = obtenerProducto(elemento)
                cantidadDetalle = cantidad[indice]
                subDetalle = subtotal[indice]
                totalDetalle = total_general[indice]

                detallePedido = DetallePedido(id_pedido=id_pedido, id_producto=objetoProducto, cantidad=cantidadDetalle
                                              , sub_total=subDetalle, total=totalDetalle)
                detallePedido.save()

            messages.success(request, 'Pedido de ID %s insertado exitosamente.' % id_pedido.id)
            return HttpResponseRedirect(reverse("appdiverxia:agregarPedido"))


# Fin de vista-----------------------------------------------------------------------------------#

# Muestra los detalles individuales de un pedido------------------------------------------------#
class VerPedido(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request, p):
        pedido = Pedido.objects.get(id=p)
        detalles = DetallePedido.objects.filter(id_pedido_id=p)
        recibido = Pedido.recibido(p)
        contexto = {'pedido': pedido, 'detalles': detalles, 'recibido': recibido}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/pedido/verPedido.html', contexto)


# Fin de vista--------------------------------------------------------------------------------------#

# Valida un pedido ya insertado------------------------------------------------#
class ValidarPedido(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request, p):
        pedido = Pedido.objects.get(id=p)
        detalles = DetallePedido.objects.filter(id_pedido_id=p)

        # Agrega los productos del pedido
        for elemento in detalles:
            elemento.id_producto.disponible += elemento.cantidad
            elemento.id_producto.save()

        pedido.presente = True
        pedido.save()
        messages.success(request, 'Pedido de ID %s verificado exitosamente.' % pedido.id)
        return HttpResponseRedirect(reverse("appdiverxia:verPedido", args=(p,)))


# Fin de vista--------------------------------------------------------------------------------------#


# Genera el pedido en CSV--------------------------------------------------------------------------#
class GenerarPedido(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request, p):
        import csv

        pedido = Pedido.objects.get(id=p)
        detalles = DetallePedido.objects.filter(id_pedido_id=p)

        nombre_pedido = "pedido_%s.csv" % (pedido.id)

        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = 'attachment; filename="%s"' % nombre_pedido
        writer = csv.writer(response)

        writer.writerow(['Producto', 'Cantidad', 'Sub-total', 'Total',
                         'Porcentaje IGV utilizado: %s' % (pedido.igv.valor_igv)])

        for producto in detalles:
            writer.writerow([producto.id_producto.descripcion, producto.cantidad, producto.sub_total, producto.total])

        writer.writerow(['Total general:', '', '', pedido.monto_general])

        return response

        # Fin de vista--------------------------------------------------------------------------------------#


# Genera el pedido en PDF--------------------------------------------------------------------------#
class GenerarPedidoPDF(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request, p):

        pedido = Pedido.objects.get(id=p)
        general = Opciones.objects.get(id=1)
        detalles = DetallePedido.objects.filter(id_pedido_id=p)

        doctipo = None
        if pedido.proveedor.documento_tipo == 1:
            doctipo = 'DNI'
        else:
            doctipo = 'RUC'
        data = {
            'fecha': pedido.fecha,
            'monto_general': pedido.monto_general,
            'nombre_proveedor': pedido.proveedor.nombre + " " + pedido.proveedor.apellido,
            'documento_proveedor': pedido.proveedor.documento,
            'documento_tipo': doctipo,
            'id_reporte': pedido.id,
            'igv': pedido.igv.valor_igv,
            'detalles': detalles,
            'modo': 'pedido',
            'general': general
        }

        nombre_pedido = "pedido_%s.pdf" % (pedido.id)

        pdf = render_to_pdf('appdiverxia/PDF/prueba.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % nombre_pedido

        return response
        # Fin de vista--------------------------------------------------------------------------------------#


# Crea un nuevo usuario--------------------------------------------------------------#
class CrearUsuario(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        if request.user.is_superuser:
            form = NuevoUsuarioFormulario()
            # Envia al usuario el formulario para que lo llene
            contexto = {'form': form, 'modo': request.session.get('usuarioCreado')}
            contexto = complementarContexto(contexto, request.user)
            return render(request, 'appdiverxia/usuario/crearUsuario.html', contexto)
        else:
            messages.error(request, 'No tiene los permisos para crear un usuario nuevo')
            return HttpResponseRedirect(reverse('appdiverxia:panel'))

    def post(self, request):
        form = NuevoUsuarioFormulario(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            rep_password = form.cleaned_data['rep_password']
            level = form.cleaned_data['level']

            error = 0

            if password == rep_password:
                pass

            else:
                error = 1
                messages.error(request, 'La clave y su repeticion tienen que coincidir')

            if usuarioExiste(Usuario, 'username', username) is False:
                pass

            else:
                error = 1
                messages.error(request, "El nombre de usuario '%s' ya existe. eliga otro!" % username)

            if usuarioExiste(Usuario, 'email', email) is False:
                pass

            else:
                error = 1
                messages.error(request, "El correo '%s' ya existe. eliga otro!" % email)

            if (error == 0):
                if level == '0':
                    nuevoUsuario = Usuario.objects.create_user(username=username, password=password, email=email)
                    nivel = 0
                elif level == '1':
                    nuevoUsuario = Usuario.objects.create_superuser(username=username, password=password, email=email)
                    nivel = 1

                nuevoUsuario.first_name = first_name
                nuevoUsuario.last_name = last_name
                nuevoUsuario.nivel = nivel
                nuevoUsuario.save()

                messages.success(request, 'Usuario creado exitosamente')
                return HttpResponseRedirect(reverse('appdiverxia:crearUsuario'))

            else:
                return HttpResponseRedirect(reverse('appdiverxia:crearUsuario'))


# Fin de vista----------------------------------------------------------------------


# Lista todos los usuarios actuales--------------------------------------------------------------#
class ListarUsuarios(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        usuarios = Usuario.objects.all()
        # Envia al usuario el formulario para que lo llene
        contexto = {'tabla': usuarios}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/usuario/listarUsuarios.html', contexto)

    def post(self, request):
        pass

    # Fin de vista----------------------------------------------------------------------


# Importa toda la base de datos, primero crea una copia de la actual mientras se procesa la nueva--#
class ImportarBDD(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        if request.user.is_superuser == False:
            messages.error(request, 'Solo los administradores pueden importar una nueva base de datos')
            return HttpResponseRedirect(reverse('appdiverxia:panel'))

        form = ImportarBDDFormulario()
        contexto = {'form': form}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/BDD/importar.html', contexto)

    def post(self, request):
        form = ImportarBDDFormulario(request.POST, request.FILES)

        if form.is_valid():
            ruta = 'appdiverxia/archivos/BDD/appdiverxia_respaldo.xml'
            manejarArchivo(request.FILES['archivo'], ruta)

            try:
                call_command('loaddata', ruta, verbosity=0)
                messages.success(request, 'Base de datos subida exitosamente')
                return HttpResponseRedirect(reverse('appdiverxia:importarBDD'))
            except Exception:
                messages.error(request, 'El archivo esta corrupto')
                return HttpResponseRedirect(reverse('appdiverxia:importarBDD'))


# Fin de vista--------------------------------------------------------------------------------


# Descarga toda la base de datos en un archivo---------------------------------------------#
class DescargarBDD(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        # Se obtiene la carpeta donde se va a guardar y despues se crea el respaldo ahi
        fs = FileSystemStorage('appdiverxia/archivos/tmp/')
        with fs.open('appdiverxia_respaldo.xml', 'w') as output:
            call_command('dumpdata', 'appdiverxia', indent=4, stdout=output, format='xml',
                         exclude=['contenttypes', 'auth.permission'])

            output.close()

        # Lo de abajo es para descargarlo
        with fs.open('appdiverxia_respaldo.xml', 'r') as output:
            response = HttpResponse(output.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'attachment; filename="appdiverxia_respaldo.xml"'

            # Cierra el archivo
            output.close()

            # Borra el archivo
            ruta = 'appdiverxia/archivos/tmp/appdiverxia_respaldo.xml'
            call_command('erasefile', ruta)

            # Regresa el archivo a descargar
            return response


# Fin de vista--------------------------------------------------------------------------------


# Configuracion general de varios elementos--------------------------------------------------#
class ConfiguracionGeneral(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request):
        conf = Opciones.objects.get(id=1)
        form = OpcionesFormulario()

        # Envia al usuario el formulario para que lo llene

        form['moneda'].field.widget.attrs['value'] = conf.moneda
        form['valor_igv'].field.widget.attrs['value'] = conf.valor_igv
        form['mensaje_factura'].field.widget.attrs['value'] = conf.mensaje_factura
        form['nombre_negocio'].field.widget.attrs['value'] = conf.nombre_negocio

        contexto = {'form': form}
        contexto = complementarContexto(contexto, request.user)
        return render(request, 'appdiverxia/opciones/configuracion.html', contexto)

    def post(self, request):
        # Crea una instancia del formulario y la llena con los datos:
        form = OpcionesFormulario(request.POST, request.FILES)
        # Revisa si es valido:

        if form.is_valid():
            # Procesa y asigna los datos con form.cleaned_data como se requiere
            moneda = form.cleaned_data['moneda']
            valor_igv = form.cleaned_data['valor_igv']
            mensaje_factura = form.cleaned_data['mensaje_factura']
            nombre_negocio = form.cleaned_data['nombre_negocio']
            imagen = request.FILES.get('imagen', False)

            # Si se subio un logo se sobreescribira en la carpeta ubicada
            # --en la siguiente ruta
            if imagen:
                manejarArchivo(imagen, 'appdiverxia/static/appdiverxia/assets/logo/logo2.png')

            conf = Opciones.objects.get(id=1)
            conf.moneda = moneda
            conf.valor_igv = valor_igv
            conf.mensaje_factura = mensaje_factura
            conf.nombre_negocio = nombre_negocio
            conf.save()

            messages.success(request, 'Configuracion actualizada exitosamente!')
            return HttpResponseRedirect(reverse("appdiverxia:configuracionGeneral"))
        else:
            form = OpcionesFormulario()
            # De lo contrario lanzara el mismo formulario
            return render(request, 'appdiverxia/opciones/configuracion.html', {'form': form})


# Fin de vista--------------------------------------------------------------------------------


# Accede a los modulos del manual de usuario---------------------------------------------#
class VerManualDeUsuario(LoginRequiredMixin, View):
    login_url = 'appdiverxia:login'
    redirect_field_name = None

    def get(self, request, pagina):
        if pagina == 'inicio':
            return render(request, 'appdiverxia/manual/index.html')

        if pagina == 'producto':
            return render(request, 'appdiverxia/manual/producto.html')

        if pagina == 'proveedor':
            return render(request, 'appdiverxia/manual/proveedor.html')

        if pagina == 'pedido':
            return render(request, 'appdiverxia/manual/pedido.html')

        if pagina == 'clientes':
            return render(request, 'appdiverxia/manual/clientes.html')

        if pagina == 'factura':
            return render(request, 'appdiverxia/manual/factura.html')

        if pagina == 'usuarios':
            return render(request, 'appdiverxia/manual/usuarios.html')

        if pagina == 'opciones':
            return render(request, 'appdiverxia/manual/opciones.html')

# Fin de vista--------------------------------------------------------------------------------
