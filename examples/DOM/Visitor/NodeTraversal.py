#
# DOM Traversal in Python
#

from xml.dom import Node

class NodeTraversal:

  def __init__(this, top):
     this.top = top
     this.visitors = []

  def addVisitor(this, visitor):
     this.visitors.append(visitor)

  def visit(this, userDefinedObject):
     this.visitInDocumentOrder(this.top, userDefinedObject)

  def notifyVisitors(this, node, userData):
     for item in this.visitors:
        if node.nodeType == Node.ATTRIBUTE_NODE:
          item.visitAttr(node, userData)
        elif node.nodeType == Node.CDATA_SECTION_NODE:
          item.visitCDATASection(node, userData)
#       elif node.nodeType == Node.CDATA_NODE:
#         item.visitCharacterData(node, userData)
        elif node.nodeType == Node.DOCUMENT_NODE:
          item.visitDocument(node, userData)
        elif node.nodeType == Node.DOCUMENT_FRAGMENT_NODE:
          item.visitDocumentFragment(node, userData)
        elif node.nodeType == Node.DOCUMENT_TYPE_NODE:
          item.visitDocumentType(node, userData)
        elif node.nodeType == Node.ELEMENT_NODE:
          item.visitElement(node, userData)
        elif node.nodeType == Node.ENTITY_NODE:
          item.visitEntity(node, userData)
        elif node.nodeType == Node.ENTITY_REFERENCE_NODE:
          item.visitEntityReference(node, userData)
        elif node.nodeType == Node.NOTATION_NODE:
          item.visitNotation(node, userData)
        elif node.nodeType == Node.PROCESSING_INSTRUCTION_NODE:
          item.visitProcessingInstruction(node, userData)
        elif node.nodeType == Node.TEXT_NODE:
          item.visitText(node, userData)

  def visitInDocumentOrder(this, node, udo):
     if node == None:
        return

     print "Visiting Node of Type",node.__class__.__name__, node.nodeType
     this.notifyVisitors(node, udo)

     if node.nodeType == Node.DOCUMENT_NODE:
        this.visitInDocumentOrder(node.documentElement, udo)

     elif node.nodeType ==  Node.ELEMENT_NODE:
	for attr in node.attributes:
            this.visitInDocumentOrder(attr, udo)

     if node.nodeType in (Node.ENTITY_REFERENCE_NODE, Node.ELEMENT_NODE):
        child = node.firstChild
        while child != None:
           this.visitInDocumentOrder(child, udo)
           child = child.nextSibling
        if node.nodeType == Node.ELEMENT_NODE:
	   for item in this.visitors:
	      item.visitEndElement(node, udo)
