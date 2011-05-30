from NodeVisitor import NodeVisitor

class Count(NodeVisitor):
  def __init__(self):
    self.numElements = 0
    self.numAttrs = 0

  def visitAttr(self, attr, userData):
    print "attribute name =",attr.name, " localName =", attr.name, " prefix =", attr.prefix
    self.numAttrs = self.numAttrs + 1

  def visitElement(self, element, userData):
    print "element ", element.tagName
    self.numElements = self.numElements + 1

  def visitEndElement(self, element, userData):
    print "end element ", element.tagName

  def visitText(self, text, userData):
    print  "text ", text.data


  def __str__(self):
    return "# Elements = %s  #Attributes = %s" % (self.numElements, self.numAttrs)
