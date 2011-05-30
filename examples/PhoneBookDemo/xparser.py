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
         self.parser = saxexts.make_parser()
      else:
         self.parser = parser
      self.xth = XTreeHandler(IgnoreWhiteSpace='yes',
                      RemoveWhiteSpace='yes',
                      CreateElementMap='yes',
                      RequireUserClasses='yes')
      for x in outer_env.keys():
         if type(outer_env[x]) == types.ClassType:
            self.xth.registerElementClass(outer_env[x])

      self.parser.setDocumentHandler(self.xth)

   def process(self, document_uri):
      Ok=None
      try:
         fp = open(sys.argv[1])
         self.parser.parseFile(fp)
         return self.xth.getDocument().getChild()
      except IOError,e:
         print "\nI/O Error: " + document_uri + ": " + str(e)
      except saxlib.SAXException,e:
         print "\nParse Error: " + document_uri  + ": " + str(e)


