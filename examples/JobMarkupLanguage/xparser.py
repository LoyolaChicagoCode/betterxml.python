#
# This is a parser that generates the document tree for you.
#
# To use this parser, create an instance of XElementParser:
#    parser = saxexts.make_parser()
#    xp = XElementParser(parser)
#
# If you have defined classes in the current environment, you might want ot
# pass this environment *to* the parser, so your classes will be created as
# tree nodes instead of the default (base) XElement class instances:
#
#
# def MyElementClass1(XElement): ...
# def MyElementClass2(XElement): ...
# ...
#
#    parser = saxexts.make_parser()
#    xp = XElementParser(parser, vars())
#
# Once your parser is constructed, you can parse one or more documents as
# follows:
#    doc_list = ['f1','f2','f3']
#     -or-
#    doc_list = ['url1','url2','url3']
#
#    for doc in doc_list:
#       doc_tree = xp.process(doc)
#       print doc_tree.toXML()


import string
import sys
import types
from xml.sax import saxexts
from xml.sax import saxlib

from xelement import XElement, XTreeHandler

class XElementParser:

   def __init__(self, outer_env={}, parser=None):
      if parser == None:
         self.parser = saxexts.XMLValParserFactory.make_parser()
      else:
         self.parser = parser
      self.parser_error_handler = ErrorPrinter()
      self.parser.setErrorHandler(self.parser_error_handler)
      self.xth = XTreeHandler(IgnoreWhiteSpace='yes',
                      RemoveWhiteSpace='yes',
                      CreateElementMap='yes',
                      RequireUserClasses='yes')
      for x in outer_env.keys():
         if type(outer_env[x]) == types.ClassType or isinstance(x, object):
            self.xth.registerElementClass(outer_env[x], x)

      self.parser.setDocumentHandler(self.xth)

   def process(self, document_uri):
      Ok=None
      try:
         self.parser_error_handler.reset()
         self.parser.parse(document_uri)
         if self.parser_error_handler.has_errors():
            raise "validation failed"
         return self.xth.getDocument().getChild()
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

