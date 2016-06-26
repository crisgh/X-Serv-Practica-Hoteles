from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models hereself.
class Hoteles(models.Model):
    Nombre = models.CharField(max_length = 300)
    categoria = models.CharField(max_length = 300)
    estrellas = models.CharField(max_length = 32)
    Descrip = models.TextField(default = "")
    direccion = models.CharField(max_length= 120)
    url_hotel = models.CharField(max_length= 120)

class Imagen(models.Model):
    url = models.CharField(max_length= 120)
    Hotel = models.ForeignKey(Hoteles)

class Comentario(models.Model):
    Date = models.DateTimeField(auto_now=True)
    body = models.TextField(default = "")
    Hotel = models.ForeignKey(Hoteles)
    Nombre_comentario = models.CharField(max_length=32)
class Hotel_selecc (models.Model):
    Nombre_usuario = models.CharField(max_length=32)
    Hotel = models.ForeignKey(Hoteles)
    Date = models.DateField(auto_now=True)


class CSS (models.Model):
    User = models.CharField(max_length = 32)
    Letra= models.IntegerField()
    Color= models.CharField(max_length = 32, default = 'black')
    Titulo = models.CharField(max_length = 32, default = 'black')
