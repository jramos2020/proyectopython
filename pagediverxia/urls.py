"""diverxia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

#app_name = "pagediverxia"
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('nosotros/', views.Nosotros.as_view(), name='nosotros'),
    path('productos/', views.Producto.as_view(), name='productos'),
    path('contacto/', views.Contacto.as_view(), name='contacto'),
    path('contacto/enviar', views.ContactoEnviar.as_view(), name='contacto.enviar')
]
