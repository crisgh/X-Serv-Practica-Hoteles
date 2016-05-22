"""final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$','hoteles.views.inicio'),
    url(r'^alojamientos$','hoteles.views.mostrarAlojamientos'),
    url(r'^alojamientos/(.+)$','hoteles.views.mostrarAlojamientoId'),
    url(r'^incluirFavorito/(.+)', 'hoteles.views.incluirFavorito'),
    url(r'^about$','hoteles.views.mostrarAbout'),
    url(r'^xml$','hoteles.views.xml_usuario'),
    url(r'^logout','django.contrib.auth.views.logout',{'next_page':'/'}),
    url(r'^login','django.contrib.auth.views.login'),
    url(r'^accounts/profile/','hoteles.views.inicio'),
    url(r'^cambiarIdioma/(.*)','hoteles.views.cambiarIdioma'),
    url(r'images/(.*)$','django.views.static.serve',{'document_root':'templates/images/'}),
    #url(r'^(estilo.css)$','django.views.static.serve',{'document_root':'templates/'}),
    url(r'(estilo.css)$','django.views.static.serve',{'document_root':'templates/'}),
    url(r'^(.*)$','hoteles.views.pagUsuario'),

    ]
