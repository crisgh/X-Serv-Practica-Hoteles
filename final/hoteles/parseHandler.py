#!/usr/bin/python

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib2,urllib
import sys
import os.path


class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.inCategoria = False
        self.inEstrellas = False
        self.theContent = ""
        self.listDic = [] #Lista de diccs, uno por cada hotel encontrado en .xml
        self.dic = {}
        self.dic['url'] = []


    def startElement (self, name, attrs):
        if name in ['name', 'body', 'web', 'address', 'zipcode', 'url']:
            self.inContent = True
            #print "estoy en start element " + name
        elif name == 'item' and attrs["name"]=="Categoria": #Hoteles, Albergues, ...
            self.inCategoria = True
            self.inContent = True
        elif name == 'item' and attrs["name"]=="SubCategoria": # Estrellas y llaves
            self.inEstrellas = True
            self.inContent = True

    def endElement (self, name):
        if name in ['name', 'body', 'web', 'address', 'zipcode']:
            self.dic[name] = self.theContent.encode('utf-8')
        elif name == 'url':
            if len(self.dic['url']) < 5:
                self.dic['url'].append(self.theContent.encode('utf-8'))
        elif name == 'item' and self.theContent and self.inCategoria:
            self.dic['categoria'] = self.theContent.encode('utf-8')
            self.inCategoria = False
        elif name == 'item' and self.theContent and self.inEstrellas:
            self.dic['estrellas'] = self.theContent.encode('utf-8')
            self.inEstrellas = False
        elif name == 'service':
            self.listDic.append(self.dic)
            self.dic = {}
            self.dic['url'] = []
        self.inContent = False
        self.theContent = ""
    def characters (self, chars):
        if self.inContent:
            self.theContent += chars
            #self.theContent = self.theContent.encode('utf-8')

    def dameLista(self):
        print self.listDic
        return self.listDic
"""
Parser = make_parser()
Handler = myContentHandler()
Parser.setContentHandler(Handler)
# Ready, set, go!
xmlFile = urllib.urlopen('http://www.esmadrid.com/opendata/alojamientos_es.xml')
Parser.parse(xmlFile)
print "Parse Complete"
"""
