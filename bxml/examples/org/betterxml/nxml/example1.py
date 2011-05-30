"""
 NaturalXML Python Edition
 
 Authors: Matt Bone and George K. Thiruvathukal

"""

import org.betterxml.nxml.nxml as natural_xml
import sys

class RootClass(object):
    def __init__(self):
        self.child = None

    def addFirstTestElement(self, test):
        self.child = test

    def get_metadata(self):
        return {
            'DocumentRootName' : 'FirstTest', 
            'DocumentRootInstance' : self.child,
            'DTDLocation' : 'http://www.thatmattbone.com/test', 
            'DTDClass' : natural_xml.DTD_CLASS_PUBLIC
        } 

    xml_metadata = property(get_metadata)

class FirstTestElement(object):
    def __init__(self):
        self.elements = []

    def addSecondTestElement(self, element):
        self.elements.append(element)

    def get_metadata(self):
        return {
            'ElementName' : self.__class__.__name__,
            'Attributes':None,
            'Children':self.elements
        }

    xml_metadata = property(get_metadata)

class SecondTestElement(object):
    def __init__(self):
        self.testAttribute = "NULL"
        self.text = ""

    def setMyAttribute(self, attribute):
        self.testAttribute = attribute

    def addText(self, text):
        self.text = self.text + text

    def get_metadata(self):
        attributes = {'OnlyAttribute':self.testAttribute}
        return {
            'ElementName' : self.__class__.__name__,
            'Attributes' : attributes,
            'Children' : None,
            "CData" : self.text
        }

    xml_metadata = property(get_metadata)


def main():    
    parser = natural_xml.NaturalXMLParser()
    parser.setDocumentRootClass(RootClass)

    parser.setElementClassMapping("FirstTestElement", FirstTestElement)
    parser.setElementClassMapping("SecondTestElement", SecondTestElement)
    parser.setElementAttributeMapping("SecondTestElement",
                                      "myattr", "MyAttribute")
    parser.setElementCDataMapping(SecondTestElement, "Text")

    try:
        tree = parser.process("example1.xml")
    except natural_xml.NaturalXMLException, inst:
        print "Error: %s" % inst
        sys.exit(2)


    f = open('output.xml', 'w')
    parser.toXML(f)

if __name__ == '__main__':
    main()
