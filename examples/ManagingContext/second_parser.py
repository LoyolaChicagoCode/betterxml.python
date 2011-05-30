import sys
import string
import types
from xml.sax import saxexts
from xml.sax import saxlib
import os.path

from UserStack import UserStack

def get_attr_map(attrs):
   attrMap = {}
   for i in range(0, len(attrs)):
       if not attrMap.has_key( attrs.getName(i) ):
          attrMap[attrs.getName(i)] = attrs.getValue(i)
   return attrMap

class VerySimpleHandler(saxlib.DocumentHandler):
   def __init__(self):
      self.friend_list = []
      self.path = '/'

   def startElement(self, name, attrs):
      attrMap = get_attr_map(attrs)
      self.path = os.path.join(self.path, name) 
      if self.path == '/Friends/Friend':
         nick_name = attrMap['nick_name']
         number = attrMap['number']
         self.friend_list.append([nick_name, number, None])
      print "startElement %s" % self.path

   def endElement(self, name):
      (self.path, dont_care) = os.path.split(self.path)
      print "endElement %s" % self.path

   def characters(self, ch, start, length):
      text = ch.strip()
      if not text: return
      if self.path == '/Friends/Friend':
         current_friend = self.friend_list[-1]
         if current_friend[-1] == None:
            current_friend[-1] = text
      print "non-whitespace character data %s" % text

      
vsh = VerySimpleHandler()
parser = saxexts.make_parser()
parser.setDocumentHandler(vsh)
try:
    parser.parse('phonebook.xml')
    for friend in vsh.friend_list:
       print friend
except IOError,e:
    print "\nI/O Error: " + document_uri + ": " + str(e)
except saxlib.SAXException,e:
    print "\nParse Error: " + document_uri  + ": " + str(e)


