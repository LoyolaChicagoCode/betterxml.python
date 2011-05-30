"""
 NaturalXML Python Edition
 
 Authors: Matt Bone and George K. Thiruvathukal

"""

import org.betterxml.nxml.nxml as natural_xml
import sys

class RootClass(object):

    def __init__(self):
        self.root = None

    def addPhonebook(self, root):
        self.root = root

    def get_metadata(self):
        return {
            'DocumentRootName' : 'Phonebook', 
            'DocumentRootInstance' : self.root,
            'DTDLocation' : 'urn://phonebook', 
            'DTDClass' : natural_xml.DTD_CLASS_PUBLIC
        } 

    xml_metadata = property(get_metadata)

"""
   Phonebook ::= Contact*
"""
class Phonebook(object):
    def __init__(self):
	self.contacts = []

    def addContact(self, element):
        print "Adding contact: ", str(element)

        self.contacts.append(element)

    def get_metadata(self):
        return {
            'ElementName' : self.__class__.__name__,
            'Attributes': None,
            'Children' : self.contacts
        }

    xml_metadata = property(get_metadata)

"""
   Contact ::= (Address | Phone)+ 
   Contact.id ::= TEXT
   Contact.name ::= TEXT
   Contact.dob ::= TEXT (or Date!)

"""
class Contact(object):
    def __init__(self):
        self.attributes = { 'id' : None, 'name' : None, 'dob' : None }
        self.phones = []
	self.addresses = []

    def setId(self, value):
        self.attributes['id'] = value

    def setName(self, value):
        self.attributes['name'] = value
        
    def setDob(self, value):
        self.attributes['dob'] = value

    def addAddress(self, item):
        self.addresses.append(item)

    def addPhone(self, item):
        self.phones.append(item)

    def get_metadata(self):
        return {
            'ElementName' : self.__class__.__name__,
            'Attributes': None,
            'Children' : tuple(self.addresses + self.phones)
        }

    xml_metadata = property(get_metadata)

    def __str__(self):
       return 'Contact: ' + str(self.attributes)

"""
   Address ::= TEXT
   Address.type ::= TEXT
"""
   
class Address(object):
    def __init__(self):
        self.type = None
	self.text = ""

    def setType(self, value):
        self.type = value

    def addText(self, text):
        self.text = self.text + text

    def get_metadata(self):
        attributes = { 'type' : self.type }
        return {
            'ElementName' : self.__class__.__name__,
            'Attributes' : attributes,
            'Children' : None,
            "CData" : self.text
        }

    xml_metadata = property(get_metadata)

class Phone(Address):
    pass

def main():    
    parser = natural_xml.NaturalXMLParser()
    parser.setDocumentRootClass(RootClass)

    parser.setElementClassMapping("Phonebook", Phonebook)
    parser.setElementClassMapping("Contact", Contact)
    parser.setElementClassMapping("Address", Address)
    parser.setElementClassMapping("Phone", Phone)

    parser.setElementAttributeMapping("Contact", "id", "Id")
    parser.setElementAttributeMapping("Contact", "name", "Name")
    parser.setElementAttributeMapping("Contact", "dob", "Dob")

    parser.setElementAttributeMapping("Address", "type", "Type")
    parser.setElementAttributeMapping("Phone", "type", "Type")

    parser.setElementCDataMapping(Address, "Text")
    parser.setElementCDataMapping(Phone, "Text")

    try:
        tree = parser.process("phonebook.xml")
    except natural_xml.NaturalXMLException, inst:
        print "Error: %s" % inst
        sys.exit(2)


    f = open('output.xml', 'w')
    parser.toXML(f)

if __name__ == '__main__':
    main()
