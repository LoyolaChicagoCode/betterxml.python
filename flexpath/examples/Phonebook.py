from org.betterxml.flexpath.FlexPath import FlexPath
from org.betterxml.flexpath.FlexFunction import *
from org.betterxml.xelement1.xelement import *
from org.betterxml.xelement1.xparser import *


if __name__ == "__main__":
    flex = FlexPath()
    
    flex.addFunction(Child, ["Foe"])
    #flex.addFunction(First)
    
    xparser = XElementParser({'Friends':XElement, 'Friend':XElement})
    doc = xparser.process("phonebook.xml")

    results = flex.evaluate([doc])
    
    print "Foes:"
    for node in results:
        print node.toXML()
        
    #print flex.functions
