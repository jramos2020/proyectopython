from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.utils.translation import gettext as _, gettext_lazy

# Create your views here.
from django.urls import reverse
from django.views.decorators.cache import never_cache


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


@never_cache
def login(self, request, extra_context=None):
    """
    Display the login form for the given HttpRequest.
    """
    if request.method == 'GET' and self.has_permission(request):
        # Already logged-in, redirect to admin index
        index_path = reverse('admin:index', current_app=self.name)
        return HttpResponseRedirect(index_path)

    # Since this module gets imported in the application's root package,
    # it cannot import models from other applications at the module level,
    # and django.contrib.admin.forms eventually imports User.
    from django.contrib.admin.forms import AdminAuthenticationForm
    from django.contrib.auth.views import LoginView
    context = {
        **self.each_context(request),
        'title': _('Log in'),
        'app_path': request.get_full_path(),
        'username': request.user.get_username(),
    }
    if (REDIRECT_FIELD_NAME not in request.GET and
            REDIRECT_FIELD_NAME not in request.POST):
        context[REDIRECT_FIELD_NAME] = reverse('admin:index', current_app=self.name)
    context.update(extra_context or {})

    defaults = {
        'extra_context': context,
        'authentication_form': self.login_form or AdminAuthenticationForm,
        'template_name': self.login_template or 'admin/login.html',
    }
    request.current_app = self.name
    return LoginView.as_view(**defaults)(request)
