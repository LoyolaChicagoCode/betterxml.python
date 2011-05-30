#
# This is intended to be an "abstract class"
#
# All methods are NOPd unless implemented.

class NodeVisitor:
   def visitAttr(self, attributes, userData):
     pass
     
   def visitCDATASection(self, cdata, userData):
     pass
     
   def visitCharacterData(self, cdata, userData):
     pass
     
   def visitDocument(self, document, userData):
     pass
     
   def visitDocumentFragment(self, documentFragment, userData):
     pass
     
   def visitDocumentType(self, documentType, userData):
     pass
     
   def visitElement(self, element, userData):
     pass
     
   def visitEndElement(self, element, userData):
     pass
     
   def visitEntity(self, entity, userData):
     pass
     
   def visitEntityReference(self, entityReference, userData):
     pass
     
   def visitNotation(self, notation, userData):
     pass
     
   def visitProcessingInstruction(self, pi, userData):
     pass
     
   def visitText(self, text, userData):
     pass
