import sys
from xml.dom.ext.reader import Sax2
DomParser = Sax2
from Count import Count
from NodeTraversal import NodeTraversal


def main():
   reader = DomParser.Reader()
   document = reader.fromStream("tasks1.xml")
   nt = NodeTraversal(document)
   c = Count()
   nt.addVisitor(c)
   nt.visit(None)
   print "Statistics:"
   print str(c)

if __name__ == '__main__':
   main()
