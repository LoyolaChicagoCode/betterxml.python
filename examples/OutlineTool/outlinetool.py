import string
import sys

from xml.sax import saxexts
from xml.sax import saxlib

from UserStack import UserStack

class XElement:
    def __init__(self, name=None, attrs=None):
        self.name = name
        self.attrs = attrs
        self.children = []
        self.text = ''

    def initialize(self):
        pass

    def finalize(self, parent):
        pass

    def linkTo(self, element):
        if isinstance(element,XElement):
            self.children.append(element)

    def cdata(self, text):
        self.text = self.text + text

    def printBFS(self, depth=0):
        print " " * depth, str(self)
        for node in self.children:
            node.printBFS(depth+1)

    def visit(self, depth):
        print " " * depth, str(self)

    def walkBFS(self, depth=0):
        self.doWalkBFS(depth)

    def doWalkBFS(self, depth=0):
        self.visit(depth)
        for node in self.children:
            node.doWalkBFS(depth+1)

    def getName(self):
        return self.name

    def getText(self):
        return self.text

    def getChildren(self, klass=None):
        if not klass:
            return self.children[:]

        children = []
        if type(klass) == type(''):
            for node in self.children:
                if node.__class__.__name__ == klass:
                    children.append(node)
        else:
            for node in self.children:
                if isinstance(node, klass):
                    children.append(node)
        return children

    def __str__(self):
        if not self.name:
            attrRep =  ''
            repr = '<>'
        else:
            attrRep = ''
            for n in range(0,len(self.attrs)):
                attrRep = attrRep + " " + self.attrs.getName(n) + "=..."
            repr = '<' + self.name + attrRep + '>'

        if len(self.children) > 0:
            repr = repr + ': ' + `len(self.children)` + ' children ' + '<'
            sep = ''
            for node in self.children:
                repr = repr + sep + node.__class__.__name__ 
                sep = ', '
            repr = repr + '>'
        repr = repr + ' text <' + self.text + '>'
        return self.__class__.__name__ + ': ' + repr

class XTreeHandler(saxlib.DocumentHandler):
    def __init__(self, **options):
        self.elems=0
        self.attrs=0
        self.pis=0
        self.contextStack = UserStack([])
        self.contextStack.push("x")
        self.document = XDocumentRoot()
        self.contextStack.push(self.document)
        self.elementMap = {}
        self.ignoreWhiteSpace = options.has_key('IgnoreWhiteSpace') \
          and options['IgnoreWhiteSpace'] in ['true','yes',1,'1']
        self.removeWhiteSpace = options.has_key('RemoveWhiteSpace') \
          and options['RemoveWhiteSpace'] in ['true','yes',1,'1']
        self.createElementMap = options.has_key('CreateElementMap') \
          and options['CreateElementMap'] in ['true','yes',1,'1']

    def getElementMap(self):
        return self.elementMap

    def startElement(self, name, attrs):
        stmt = 'element = ' + name + '(name,attrs)'
        try:
            exec stmt
        except:
            element = XElement(name,attrs)

        if self.createElementMap:
            if not self.elementMap.has_key(name):
                self.elementMap[name] = []
            self.elementMap[name].append(element)

        element.initialize()

        self.contextStack.top().linkTo(element)

        self.contextStack.push(element)
        self.elems=self.elems+1
        self.attrs=self.attrs+len(attrs)

    def endElement(self, name):
        popElement = self.contextStack.pop()
        popElement.finalize(self.contextStack.top())

    def characters(self, ch, start, length):
        tos = self.contextStack.top()
        if self.removeWhiteSpace:
            text = ch[start:start+length]
            splitText = string.split(text)
            if len(tos.text) > 0:
                pad = ' '
            else:
                pad = ''
            for item in splitText:
                tos.cdata(pad + item)
                pad = ' '
        else:
            tos.cdata(ch[start:start+length])

    def ignorableWhitespace(self, ch, start, length):
        print "ignorable ws encountered"
        if not self.ignoreWhiteSpace:
            self.contextStack.top().cdata(ch[start:start+length])

    def getDocument(self):
        return self.document

    def processingInstruction(self,target,data):
        self.pis=self.pis+1

class XDocumentRoot(XElement):
    def __init__(self):
        XElement.__init__(self)

    def endElement(self):
        print "Document contains %d elements." % (len(self.children))

class Abstract(XElement):
    def __init__(self,name,attrs):
        XElement.__init__(self,name,attrs)

class Outline(XElement):
    def __init__(self,name,attrs):
        self.allText = ''
        XElement.__init__(self,name,attrs)

    def getAllText(self):
        return self.allText

    def addText(self, text):
        if len(self.allText):
            self.allText = self.allText + ' ' + text
        else:
            self.allText = text

class Item(XElement):
    def __init__(self,name,attrs):
        self.allText = ''
        XElement.__init__(self,name,attrs)

    def addText(self, text):
        if len(self.allText):
            self.allText = self.allText + ' ' + text
        else:
            self.allText = text

    def finalize(self, parent):
        parent.addText(self.text)

class Content(XElement):
    def __init__(self,name,attrs):
        print "creating Content XElement instance"
        XElement.__init__(self,name,attrs)

class Requires(XElement):
    def __init__(self,name,attrs):
        XElement.__init__(self,name,attrs)

class Uses(XElement):
    def __init__(self,name,attrs):
        XElement.__init__(self,name,attrs)

class Defines(XElement):
    def __init__(self,name,attrs):
        XElement.__init__(self,name,attrs)

class Keywords(XElement):
    def __init__(self,name,attrs):
        XElement.__init__(self,name,attrs)

class Topic(XElement):
    def __init__(self,name,attrs):
        XElement.__init__(self,name,attrs)

    def finalize(self, parent):
        self.id = self.attrs.get('id','none specified')
        abstract = self.getChildren(Abstract)
        requires = self.getChildren(Requires)
        outline = self.getChildren(Outline)
        uses = self.getChildren(Uses)
        keywords = self.getChildren(Keywords)

        if len(abstract):
            self.abstract = abstract[0].getText()
        else: self.abstract = ''

        if len(requires):
            self.requires = string.split(requires[0].getText())
        else: self.requires = []

        if len(outline):
            self.words = string.split(outline[0].getAllText())
        else: self.words = ''

        if len(uses):
            self.uses = string.split(uses[0].getText())
        else: self.uses = []

        if len(keywords):
            self.keywords = string.split(keywords[0].getText())
        else: self.keywords = []

    def __str__(self):
        return 'Topic %s\nAbstract\n%s\nkeywords\n%s\nreq\n%s\nuses\n%s\nwords used\n%s\n' % (self.id, self.abstract, `self.keywords`, `self.requires`, `self.uses`, `self.words`)


def analyzeTopics(topics):
    kwMap = {}
    wordMap = {}
    usedMap = {}
    undefMap = {}

    for topic in topics:
        print "* Analyzing Topic %s" % topic.id
        for word in topic.requires:
            print "\t- %s:" % word
            if kwMap.has_key(word):
                print "\t\t+ defined in <keyword> section for these topics:"
                for whereSeen in kwMap[word]:
                    if whereSeen != topic: print "\t\t\t%s" % whereSeen.id
            else:
                if wordMap.has_key(word):
                    print "\t\t= not defined but found in <outline> in earlier topic(s):"
                    for whereSeen in wordMap[word]:
                        if whereSeen != topic: print "\t\t\t%s" % whereSeen.id

                elif usedMap.has_key(word):
                    print "\t\t- not defined but found used (section <used>) in earlier topic(s):"
                    for whereSeen in usedMap[word]:
                        if whereSeen != topic: print "\t\t\t%s" % whereSeen.id

                elif undefMap.has_key(word):
                    print "\t\t- already reported undefined for earlier topic(s):"
                    for whereSeen in undefMap[word]:
                        if whereSeen != topic: print "\t\t\t%s" % whereSeen.id
                else:
                    print "\t\t- not found in any preceding topic (in any section)"

                if not undefMap.has_key(word):
                    entry = undefMap[word] = []
                else:
                    entry = undefMap[word]
                entry.append(topic)

            print 
        for word in topic.keywords:
            if not kwMap.has_key(word):
                entry = kwMap[word] = []
            else:
                entry = kwMap[word]
            entry.append(topic)
        for word in topic.words:
            if not wordMap.has_key(word):
                entry = wordMap[word] = []
            else:
                entry = wordMap[word]
            entry.append(topic)

        for word in topic.uses:
            if not entry:
                entry = usedMap[word] = []
            else:
                entry = usedMap[word]
            entry.append(topic)


    print "* All Defined Topics"
    for kw in kwMap.keys():
        print "\t",kw

    print "* All Undefined Topics"
    for kw in undefMap.keys():
        print "\t",kw

    print "* All Used Topics"
    for kw in usedMap.keys():
        print "\t",kw

    print "* Checking for undefined Topics that got defined later:"
    print "  each line output is (missing word, where identified, where defined)"
    for word in kwMap.keys():
        if undefMap.has_key(word):
            for topic_i in undefMap[word]:
                for topic_j in kwMap[word]:
                    print "\t(%s, %s, %s)" % (word, topic_i.id, topic_j.id)
            del(undefMap[word])

    print "* New List of Undefined Topics"            
    for kw in undefMap.keys():
        print "\t",kw

def go():
   if len(sys.argv) < 2:
      print "Usage: python saxtree.py <document>"
      print
      print " <document>: file name of the document to parse"
      sys.exit(1)

   p = saxexts.make_parser()
   xth = XTreeHandler(IgnoreWhiteSpace='yes',RemoveWhiteSpace='yes',CreateElementMap='yes')
   p.setDocumentHandler(xth)

   Ok=None
   try:
      p.parse(sys.argv[1])
      print "Parse complete:"
      print "  Elements:    %d" % xth.elems
      print "  Attributes:  %d" % xth.attrs
      print "  Proc instrs: %d" % xth.pis
      print "  elements:    %s" % `xth.getElementMap().keys()`

      document = xth.getDocument()

      print "  Document has %d children " % len(document.getChildren())
      content = document.getChildren('Content')
      topics = content[0].getChildren('Topic')
      print "%d content objects" % len(content)
      print "%d topic objects" % len(topics)
      topics = content[0].getChildren(Topic)
      print "%d topic objects" % len(topics)
      analyzeTopics(topics)
   except IOError,e:
      print "\nERROR: "+sys.argv[1]+": "+str(e)
   except saxlib.SAXException,e:
      print "\nERROR: "+str(e)


# Main Program

if __name__ == '__main__':
   go()
