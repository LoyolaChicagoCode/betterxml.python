import string
import sys
import types
from xml.sax import saxexts
from xml.sax import saxlib

from pelement_sax import PElement, PElementHandler

class PElementParser:

   def __init__(self, dir_name, parser=None):
      if parser == None:
         self.parser = saxexts.XMLValParserFactory.make_parser()
      else:
         self.parser = parser
      self.parser_error_handler = ErrorPrinter()
      self.parser.setErrorHandler(self.parser_error_handler)
      self.xth = PElementHandler(dir_name)
      self.dir_name = dir_name
      self.parser.setDocumentHandler(self.xth)

   def process(self, document_uri):
      Ok=None
      try:
         self.parser_error_handler.reset()
         self.parser.parse(document_uri)
         if self.parser_error_handler.has_errors():
            raise "validation failed"
         return self.xth.getDocument()
      except IOError,e:
         print "\nI/O Error: " + document_uri + ": " + str(e)
      except saxlib.SAXException,e:
         print "\nParse Error: " + document_uri  + ": " + str(e)


class ErrorPrinter:
    "A simple class that just prints error messages to standard out."

    def __init__(self):
       self.error_count = 0

    def reset(self):
       self.error_count = 0

    def has_errors(self):
       return self.error_count

    def warning(self, exception):
       print "Warning: %s %s" % (str(exception), exception.getMessage())
       sys.exit(1)

    def error(self, exception):
       self.error_count = self.error_count + 1
       print "Error: %s %s" % (str(exception), exception.getMessage())

    def fatalError(self, exception):
       self.error_count = self.error_count + 1
       print "Fatal Error: %s %s" % (str(exception), exception.getMessage())

