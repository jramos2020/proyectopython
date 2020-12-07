from django.http import JsonResponse
from django.shortcuts import render
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
    from django.core import mail
    connection = mail.get_connection()

    # Manually open the connection
    connection.open()

    remitente = "Chuculum <jramos@luisml.com>"
    destinatario = "Chuculum <juhanramos3@gmail.com>"
    # destinatario = "%s <%s>"%(data.nombre,data.correo)
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

    email = """From: %s 
    To: %s 
    MIME-Version: 1.0 
    Content-type: text/html 
    Subject: %s 

    %s
    """ % (remitente, destinatario, asunto, mensaje)
    # try:
    # smtp = smtplib.SMTP_SSL('mail.mevisoft.com',465)
    # smtp.ehlo()
    # smtp.login('jramos@luisml.com','@passwordjramos')
    # smtp.sendmail(remitente, destinatario, email)
    return JsonResponse({'message': "Correo enviado"})

# except:
#    return JsonResponse({'message': """Error: el mensaje no pudo enviarse.
#    Compruebe que sendmail se encuentra instalado en su sistema"""})
