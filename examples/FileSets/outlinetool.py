import string
import sys

from xml.sax import saxexts
from xml.sax import saxlib
import types

from xelement import XElement, XTreeHandler

class Abstract(XElement): pass

class Outline(XElement):
    def initialize(self):
        self.allText = ''

    def getAllText(self):
        return self.allText

    def addText(self, text):
        if len(self.allText):
            self.allText = self.allText + ' ' + text
        else:
            self.allText = text

class Item(XElement):
    def initialize(self):
        self.allText = ''

    def addText(self, text):
        if len(self.allText):
            self.allText = self.allText + ' ' + text
        else:
            self.allText = text

    def finalize(self, parent):
        parent.addText(self.text)

class Content(XElement):
    def initialize(self):
        print "creating Content XElement instance"

class Requires(XElement): pass

class Uses(XElement): pass

class Defines(XElement): pass

class Keywords(XElement): pass

class Topic(XElement):
    def finalize(self, parent):
        self.id = self.attrs.getFirst('id','none specified')
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

def go(outer_env):
   if len(sys.argv) < 2:
      print "Usage: python saxtree.py <document>"
      print
      print " <document>: file name of the document to parse"
      sys.exit(1)

   p = saxexts.make_parser()
   xth = XTreeHandler(IgnoreWhiteSpace='yes',
                      RemoveWhiteSpace='yes',
                      CreateElementMap='yes')
   for x in outer_env.keys():
      if type(outer_env[x]) == types.ClassType:
         print "registering %s" % x
         xth.registerElementClass(outer_env[x])
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
      prologue = []
      prologue.append('<?xml>')
      prologue.append('<!-- Outline Tool by George K. Thiruvathukal -->')
      print content[0].toXML(prologue=prologue, indent_text="  ")
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
   go( vars() )
