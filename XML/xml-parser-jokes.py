#!/usr/bin/python

#
# Simple XML parser for JokesXML
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the jokes in a JokesXML file

from xml.sax.handler import ContentHandler  #Los elementos tienen el comportamiento que yo quiero
from xml.sax import make_parser             #Fabrica parses XML
import sys
import string

def normalize_whitespace(text):                     #Normaliza espacios en blanco. Por estética
    "Remove redundant whitespace from a string"
    return string.join(string.split(text), ' ')

class CounterHandler(ContentHandler):

    def __init__ (self):
        self.inContent = 0          #1 si lee contenido que me interesa, y 0 si no me interesa
        self.theContent = ""        #Guardo el contenido que me interesa

    def startElement (self, name, attrs):
        if name == 'joke':
            self.title = normalize_whitespace(attrs.get('title'))
            print " title: " + self.title + "."
        elif name == 'start':
            self.inContent = 1
        elif name == 'end':
            if self.first:
                self.inContent = 1

    def endElement (self, name):
        if self.inContent:
            self.theContent = normalize_whitespace(self.theContent)     #Estoy al final del elemento, y como he dicho que me interesaba se ha
                                                                        #guardado el texto, y normalizo los espacios para luego escribirlo
        if name == 'joke':
            print ""
        elif name == 'start':
            print "  start: " + self.theContent + "."
        elif name == 'end':
            print "  end: " + self.theContent + "."
        if self.inContent:                                              #Vuelvo a vaciar theContent y vuelvo a ponerlo a 0
            self.inContent = 0
            self.theContent = ""

    def characters (self, chars):               #Guarda los caracteres cuando inContent es 1
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog

if len(sys.argv)<2:
    print "Usage: python xml-parser-jokes.py <document>"
    print
    print " <document>: file name of the document to parse"
    sys.exit(1)

# Load parser and driver

JokeParser = make_parser()                      #Crea un parser SAX
JokeHandler = CounterHandler()                  #Crea un manejador de eventos, pero no he dicho que quiero hacer
JokeParser.setContentHandler(JokeHandler)       #Aqui le doy el comportamiento

# Ready, set, go!

xmlFile = open(sys.argv[1],"r")                 #Abro el fichero
JokeParser.parse(xmlFile)                       #parse es un método de JokeParser

print "Parse complete"
