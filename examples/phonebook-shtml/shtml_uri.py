import sys
import os
import os.path

sys.path.append('../../..')

from org.betterxml.xelement2.xelement2 import XElement
 
def getNamespaceURI():
   return "http://w3c.org/HTML"

def getDefaultElementClass():
   return XElement

def getMappings():
   return { 'html' : HTML, 'i': Italics, 'a' : Anchor }

class HTML(XElement): pass

class Italics(XElement): pass

class Anchor(XElement): pass

