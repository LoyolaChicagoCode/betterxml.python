"""
XElement is a DOM that makes sense for Python. We use the SAX interface to
build the XElement tree.

"""
import string
import sys
import types
import os

from xml.sax import saxexts
from xml.sax import saxlib

from UserStack import UserStack
from PXML import PElement

class PElementHandler(saxlib.DocumentHandler):
    def __init__(self, dir_name):
       self.dir_name = dir_name
       self.dir_path = os.path.abspath(dir_name)
       self.contextStack = UserStack([])
       pe = PElement(dir_name)
       self.contextStack.push(pe)


    def startElement(self, name, attrs):
        pe = self.contextStack.top()
        pe.add_element(1)
        e = pe.get_element(-1)
        e.set_name(name)
        for i in range(0, len(attrs)):
           attr_name = attrs.getName(i)
           attr_value = attrs.getValue(i)
           e.add_attribute(attr_name, attr_value)
        self.contextStack.push(e)

    def endElement(self, name):
        popElement = self.contextStack.pop()

    def characters(self, ch, start, length):
        text = ch[start:start+length]
        text = text.strip()
        if not text: return
        pe = self.contextStack.top()
        pe.add_cdata_element()
        te = pe.get_element(-1)
        te.set_text(text)

    def ignorableWhitespace(self, ch, start, length):
        pass

    def getDocument(self):
        return self.contextStack.top()

    def processingInstruction(self,target,data):
        pass

