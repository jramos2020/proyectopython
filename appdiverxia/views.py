from django.http import JsonResponse
from django.shortcuts import render, redirect
import smtplib


# Create your views here.
def index(request):
    # return render(request,"paginadiverxia/index.html")
    return render(request, "index.html")


def nosotros(request):
    # return render(request,"paginadiverxia/index.html")
    return render(request, "nosotros.html")


def producto(request):
    # return render(request,"paginadiverxia/index.html")
    return render(request, "producto.html")


def contacto(request):
    # return render(request,"paginadiverxia/index.html")
    return render(request, "contacto.html")


def contactoEnviar(request):
    data = request.POST

    from django.core.mail import send_mail

    asunto = "Formulario Contacto"
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
