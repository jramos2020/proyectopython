from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.utils.translation import gettext as _, gettext_lazy

# Create your views here.
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views import View


class Index(View):
    def get(self, request):
        return render(request, "pagediverxia/index.html")


class Nosotros(View):
    def get(self, request):
        return render(request, "pagediverxia/nosotros.html")


class Producto(View):
    def get(self, request):
        return render(request, "pagediverxia/producto.html")


class Contacto(View):
    def get(self, request):
        return render(request, "pagediverxia/contacto.html")


class ContactoEnviar(View):
    def post(self, request):
        data = request.POST

        from django.core.mail import send_mail

        asunto = "Formulario Contacto Web"
        mensaje = """Nuevo Contactanos:!<br/> <br/> 
        Nombre: %s <br>
        Email: %s  <br>
        Celular: %s <br>
        Mensaje: %s
        """ % (data['nombre'], data['correo'], data['celular'], data['mensaje'])

        send_mail(
            asunto,
            mensaje,
            'jramos@luisml.com',
            ['juhanramos3@gmail.com'],
            fail_silently=False,
        )

        return redirect('contacto')


