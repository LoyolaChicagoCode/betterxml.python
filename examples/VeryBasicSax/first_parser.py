import sys
import string
import types
from xml.sax import saxexts
from xml.sax import saxlib

class VerySimpleHandler(saxlib.DocumentHandler):

   def startElement(self, name, attrs):
      print "startElement(%s, %s)" % (name, attrs)
      for i in range(0, len(attrs)):
         print " - (%s, %s)" % (attrs.getName(i), attrs.getValue(i))

   def endElement(self, name):
      print "endElement(%s)" % name

   def characters(self, ch, start, length):
      print "character data %s %d %d" % (ch, start, length)
      print " -> ",ch[start:start+length]
      
vsh = VerySimpleHandler()
parser = saxexts.make_parser()
parser.setDocumentHandler(vsh)
try:
    f = open(sys.argv[1])
    parser.parseFile( f )
except IOError,e:
    print "\nI/O Error: " + document_uri + ": " + str(e)
except saxlib.SAXException,e:
    print "\nParse Error: " + document_uri  + ": " + str(e)


