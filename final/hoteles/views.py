from __future__ import unicode_literals
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib2
import sys

import os.path
from parseHandler import myContentHandler
from models import Hoteles, Imagen, Comentario, Hotel_selecc, CSS
from django.contrib.auth.models import User
from django.shortcuts import redirect , render_to_response # Redireccion
from operator import itemgetter # te ordena para los comentrios
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.core.context_processors import csrf
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.timezone import now
from django.utils.html import strip_tags
# Create your views here.

@csrf_exempt
def parsear(idioma):
    # Load parser and driver
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    # Ready, set, go!
    if idioma == 'es':
        xmlFile = urllib2.urlopen('http://www.esmadrid.com/opendata/alojamientos_es.xml')
        xmlFile = urllib2.urlopen('http://cursosweb.github.io/etc/alojamientos_es.xml')

    if idioma == 'en':
        #xmlFile = urllib2.urlopen('http://www.esmadrid.com/opendata/alojamientos_v1_en.xml')
        xmlFile = urllib2.urlopen('http://cursosweb.github.io/etc/alojamientos_en.xml')

    if idioma == 'fr':
        #xmlFile = urllib2.urlopen('http://www.esmadrid.com/opendata/alojamientos_v1_fr.xml')
        xmlFile = urllib2.urlopen('http://cursosweb.github.io/etc/alojamientos_fr.xml')

    theParser.parse(xmlFile)
    lista = theHandler.dameLista()
    print "Parse " + idioma + " complete"
    return lista


def inicio(request):
    if request.user.is_authenticated():
        logged = True
    else:
        logged = False
    respuesta = ""
    list_ordenada = []
    list_users = []
    alojamientos = Hoteles.objects.all()
    if len(alojamientos)<1 :
        lista_es = parsear('es')
        respuesta = iniHoteles(lista_es)
        return redirect("/")
    # Si la lista de hoteles es menor que 1 parsea y si no nada
    list_ordenada = ordenarhoteles(alojamientos)
    contador = 0
    lista_hoteles = []
    for elem in list_ordenada:
        if contador < 10:
            contador = contador + 1
            try:
                alojamiento = Hoteles.objects.get(id = elem[0])
                imagenes = Imagen.objects.filter(Hotel_id = alojamiento)
                usuarios = User.objects.all()
                for usuario in usuarios:
                    try:
                        css = CSS.objects.get(User = usuario.username)
                        if len(list_users)<len(usuarios):
                            list_users.append((css.User, css.Titulo))
                    except CSS.DoesNotExist:
                        if len(list_users)<len(usuarios):
                            list_users.append((usuario.username, ("Pagina de " + usuario.username)))
                if len(imagenes)>0:
                    lista_hoteles.append((alojamiento, imagenes[0].url))
                else:
                    lista_hoteles.append((alojamiento, ""))
            except ObjectDoesNotExist:
                    print "No existe el alojamiento!"

    template = get_template('plantilla_index.html')
    Context = RequestContext(request, {'hoteles':lista_hoteles ,
                                        'username':request.user.username,
                                        'users':list_users,
                                        'logged' : logged,
                                        })
    return HttpResponse(template.render(Context))
    print list_users


def iniHoteles(lista):

    reload(sys)
    sys.setdefaultencoding('utf8')
    respuesta = ""
    for dicHotel in lista:
        nombre = dicHotel['name']
        direccion = dicHotel['address'] + ', ' + dicHotel['zipcode']
        categoria = dicHotel['categoria'] + "\n"
        try:
            estrellas = dicHotel['estrellas']
        except KeyError:
            respuesta += ""
        url = dicHotel['web']
        descripcion = strip_tags(dicHotel['body'])
        hotel = Hoteles(Nombre = nombre, direccion = direccion, categoria = categoria, estrellas = estrellas, url_hotel = url, Descrip = descripcion)
        hotel.save()
        list_imag = dicHotel['url']
        if not list_imag==[]:
            for url in list_imag:
                imagen = Imagen(url = url, Hotel = hotel)
                imagen.save()
    return respuesta

#Ordena la lista de alojamientos por de numero de comentarios de mayor a menor
def ordenarhoteles(lista):
    dic = {}
    lis_ordenada = []
    respuesta = ""
    for alojamientos in lista:
        identificador = alojamientos.id
        try:
            comentarios = Comentario.objects.filter(Hotel_id = identificador) # puede que salte fallo mirar en la tabala seria " Hotel"
            dic[identificador] =len(comentarios)
        except Comentario.DoesNotExist:
            respuesta += "No tiene comentarios"
    lis_ordenada = sorted(dic.items(), key = itemgetter(1), reverse = True)
    return lis_ordenada

def pagUsuario(request,usuario):
    if request.user.is_authenticated():
        logged = True
        nombreUser = request.user.username

    else:
        logged = False
        nombreUser = "usuario"
    hoteles = []
    #username = request.user.username
    try:
        css = CSS.objects.get(User=usuario)
        titulo = css.Titulo
        u = usuario
        usuario = User.objects.get(username=usuario)
    except CSS.DoesNotExist:
        usuario = User.objects.get(username=usuario)
        u = usuario.username
        titulo = ""
    if nombreUser == usuario:
        try:
            hoteles = Hotel_selecc.objects.filter(Nombre_usuario=usuario)
        except Hotel_selecc.DoesNotExist:
            print "No hay hoteles favoritos"
            return redirect("/")
    else:
        try:
            user = User.objects.filter(username=usuario)
            hoteles = Hotel_selecc.objects.filter(Nombre_usuario=usuario)

        except Hotel_selecc.DoesNotExist:
            print "No hay hoteles favoritos"
            hoteles = [""]

    template = get_template('pagUsuario.html')
    context = RequestContext(request, {'hoteles': hoteles, 'username':nombreUser,'usuario': u, 'titulo': titulo,'logged':logged}) #le pasamos el objeto completo
    return HttpResponse(template.render(context))

def cambiarTitulo(request):
    hoteles = []
    if request.user.is_authenticated():
        logged = True
        nombreUser = request.user.username
        titulo = request.POST.get("titulo")
        #letra = request.POST.get("Letra")
        #color = request.POST.get("Color")
        try:
            css = CSS.objects.get(User=nombreUser)
            css.Titulo = titulo
            #css.Letra = letra
            #css.Color = color
            css.save()
            print "aqui"
            usuario = User.objects.get(username=nombreUser)
        except CSS.DoesNotExist:
            print "no existe"
            css = CSS(Titulo=titulo, User=nombreUser, Letra=0.0, Color="#DF01A5")
            css.save()
            usuario = User.objects.get(username=nombreUser)
    if nombreUser == usuario:
        try:
            hoteles = Hotel_selecc.objects.filter(Nombre_usuario=usuario)
        except Hotel_selecc.DoesNotExist:
            print "No hay hoteles favoritos"
            return redirect("/")
    else:
        try:
            user = User.objects.filter(username=usuario)
            hoteles = Hotel_selecc.objects.filter(Nombre_usuario=usuario)
        except Hotel_selecc.DoesNotExist:
            print "No hay hoteles favoritos"
            hoteles = [""]

    template = get_template('pagUsuario.html')
    context = RequestContext(request, {'hoteles': hoteles, 'username': nombreUser, 'titulo': titulo,
                                        #'Letra':letra,
                                        #'Color':color,
                                        'logged':logged}) #le pasamos el objeto completo
    return HttpResponse(template.render(context))
    return redirect("/" + username)

def xml_usuario(request):
    if request.user.is_authenticated():
        logged = True
        nombreUser = request.user.username
        print nombreUser
        #user=User.objects.filter(username=nombreUser)
        #print user
        Hotel = Hotel_selecc.objects.filter(Nombre_usuario=nombreUser)
        print Hotel
        data = serializers.serialize("xml", Hotel)
        from django.core.files import File
        f = open('usuario.xml', 'w')
        myfile = File(f)
        myfile.write(data)
        myfile.close()
        fil = open('usuario.xml','r')
        xml = fil.read()
    else:
        logged = False

    return HttpResponse(xml,content_type = 'text/xml')

def incluirFavorito(request,ident):
    respuesta = "Favorito incluido en tu lista "
    if request.user.is_authenticated():
        nombreUser = request.user.username
        try:
            user = User.objects.get(username = nombreUser)
            alojamiento = Hoteles.objects.get(id = int(ident))
            favorito = Hotel_selecc(Hotel = alojamiento, Nombre_usuario = user)
            favorito.save()
            #return redirect("/alojamientos/"+ id)
        except ObjectDoesNotExist:
            respuesta += "Error al incluir favorito"
    else :
        respuesta += ("No hay usuario registrado. -> registrate y podras !")
        return HttpResponse(respuesta)
    return redirect("/")


def mostrarAlojamientos(request):
    if request.user.is_authenticated():
        logged = True
    else:
        logged = False
    #if 'filt' in request.POST and request.POST['filt']:
    if request.method == 'POST':
        filt = request.POST['filt']
        grupo = request.POST['estrellas']
        print filt + grupo
        try:
            hoteles_fil = Hoteles.objects.filter(categoria__contains=filt)
            hoteles_fil = hoteles_fil.filter(estrellas__contains=grupo)

        except Hoteles.DoesNotExist:
            print  "no hay hoteles con esa categoria "
            return redirec("/alojamientos")
        template = get_template('alojamientos.html')
        Context = RequestContext(request,{'hoteles':hoteles_fil,'username':request.user.username,'logged':logged,'filt':filt,})
        #return redirect ("/alojamientos")
    else :
        filt = "None"
        hoteles = Hoteles.objects.all()
        template = get_template('alojamientos.html')
        Context = RequestContext(request, {'hoteles':hoteles ,
                                            'username':request.user.username,
                                            'logged' : logged,
                                            'filt': filt,
                                            })

    return HttpResponse(template.render(Context))

def mostrarAlojamientoId(request, ident):
    if request.user.is_authenticated():
        logged = True
        nombreUser = request.user.username
        try:
            user = User.objects.get(username = nombreUser)
        except User.DoesNotExist:
            print "Fallo aqui"

    else:
        logged = False
        nombreUser = "usuario"
    hotel = Hoteles.objects.get(id=int(ident))
    encontrado = True
    buscar = True
    if request.method == 'POST':
        comentario = Comentario(body = request.POST['comment'], Hotel_id = int(ident), Nombre_comentario = nombreUser)
        if buscar == True:
            try:
                comentario = Comentario.objects.get(Hotel_id = int(ident),Nombre_comentario=nombreUser)
                print "busco y existe"
            except Comentario.DoesNotExist:
                encontrado = False
        if encontrado == False:
            comentario.save()
            print "guardo"
    try:
        hotel= Hoteles.objects.get(id=ident)
        imagenes = Imagen.objects.filter(Hotel_id=ident)
        comentario = Comentario.objects.filter(Hotel_id=ident)
    except Hoteles.DoesNotExist:
        return redirect("/alojamientos")
#respuesta += '<li><a href="/incluirFavorito">Incluir este alojamiento en Favoritos :)</a></li>'
    #except Comentario.DoesNotExist:
    #    comentario = ""
    template = get_template('alojamientoId.html')

    Context = RequestContext (request,{  'username': nombreUser,
                                            'logged': logged,
                                            'hotel': hotel,
                                            'imagenes': imagenes,
                                            'comentarios':comentario,})
    return HttpResponse(template.render(Context))

def mostrarCss(request):
    if request.user.is_authenticated():
        logged = True
    else:
        logged = False
    template = get_template('about.html')
    context = ({'username': request.user.username,
                'logged': logged})
    return HttpResponse(template.render(context))

def mostrarAbout(request):
    if request.user.is_authenticated():
        logged = True
    else:
        logged = False
    template = get_template('about.html')
    context = ({'username': request.user.username,
                'logged': logged})
    return HttpResponse(template.render(context))
def cambiarIdioma(request, ident):
    if request.user.is_authenticated():
        logged = True
    else:
        logged = False
    lista = []
    idioma = request.POST.get("idioma")

    alojamiento = Hoteles.objects.get(id=ident)
    imagenes = Imagen.objects.filter(Hotel_id = alojamiento)
    comentarios = Comentario.objects.filter(Hotel_id=alojamiento)
    nombre = alojamiento.Nombre
    if len(imagenes)==0:
        imagenes = []
    if len(comentarios)==0:
        comentarios = []

    if idioma=="ingles":
        print "entra"
        lista = parsear("en")
        print lista
        for elem in lista:
            if elem["name"]==nombre:
                body = elem["body"]
                print body
                alojamiento.Descrip = body
        template = get_template('alojamientoId.html')
        context = RequestContext(request, {'username': request.user.username,'hotel': alojamiento, 'imagenes': imagenes, 'comentarios': comentarios, 'logged':logged}) #le pasamos el objeto completo
        return HttpResponse(template.render(context))
    if idioma=="frances":
        lista = parsear('fr')
        for elem in lista:
            if elem["name"]==nombre:
                body =elem["body"]
                alojamiento.Descrip = body
        template = get_template('alojamientoId.html')
        context = RequestContext(request, {'username': request.user.username,'hotel': alojamiento, 'imagenes': imagenes, 'comentarios': comentarios,'logged':logged}) #le pasamos el objeto completo
        return HttpResponse(template.render(context))
    if idioma=="espaniol" or "None":
        return redirect("/alojamientos/" + str(ident))

def RSS(request):
    if request.user.is_authenticated():
        logged = True
        nombreUser = request.user.username
        try:
            user = User.objects.get(username = nombreUser)
        except User.DoesNotExist:
            print "Fallo aqui"

    else:
        logged = False
        nombreUser = ""
    comentarios = Comentario.objects.all()
    template = get_template('rss.html')
    context = RequestContext(request, {'logged':logged,'username':nombreUser,'comentarios': comentarios})
    return HttpResponse(template.render(context))
