import unittest
import sys

#sys.path.insert(0, '../../../../../better-xml-python/src')
from org.betterxml.xelement1.xelement import XElement

sys.path.append('../../../../src')
from org.betterxml.flexpath.FlexFunction import *
from org.betterxml.flexpath.Exceptions import *

class ChildTest(unittest.TestCase):   
    def testValidateArgs(self):

        #too many args, should fail
        self.args = ["X","Y"]
        try:
            Child(self.args);
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            #assertTrue(ifa.getMessage().contains("Child only takes 0 or 1 argument."))
            pass
        
        #test with 1 argument, should be fine
        self.args = ["X"]
        try:
            Child(self.args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        #test with 0 arguments, should be fine
        self.args = []
        try:
            Child(self.args);
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        #test with null arguments, should be fine
        self.args = None
        try:
            Child(self.args);
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
    
    def currentResults(self):
        test = XElement("test")
        x1 =  XElement("X")
        x2 = XElement("X")
        x3 = XElement("X")
        y = XElement("Y")
        
        children = [x1, y, x2, x3]
        test.setChildren(children)

        return [test]
    
    def testEvaluate(self):
        
        #just get children elements X
        args = ["X"]
        child = None
        try:
            child = Child(args);
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = child.evaluate(self.currentResults())
        self.assertEquals(3, len(results));
        for node in results:
            self.assertEquals(node.__class__, XElement)
            self.assertEquals("X", node.getName())
        
        
        #Just get children elements Y
        args = ["Y"]
        child = None
        try:
            child = Child(args)
        except InvalidFunctionArguments, ifa:
            fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = child.evaluate(self.currentResults())
        self.assertEquals(1, len(results))
        for node in results:
            self.assertEquals(node.__class__, XElement)
            self.assertEquals("Y", node.getName())
        
        
        #get children of elements Z, there should be none of these
        args = ["Z"]
        child = None
        try:
            child = Child(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = child.evaluate(self.currentResults())
        self.assertEquals(0, len(results))

        #get children of element Y with a null currentResults -- should return null
        child = None
        args = list()
        try:
            child = Child(None)
        except InvalidFunctionArguments, ifa:
            fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = child.evaluate(None);
        self.assertEquals(None, results);
        
        #get all children by passing in an empty args string at construction, should be 4 and in order
        args = []
        child = None
        try:
            child = Child(args)
        except InvalidFunctionArguments, ifa:
            fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = child.evaluate(self.currentResults())
        self.assertEquals(4, len(results))
        
        self.assertEquals("X", results[0].getName())
        self.assertEquals("Y", results[1].getName())
        self.assertEquals("X", results[2].getName())
        self.assertEquals("X", results[3].getName())

        #get all children by passing in a null args string at construction, should be 4 and in order
        child = None
        try:
            child = Child(None);
        except InvalidFunctionArguments, ifa:
            fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = child.evaluate(self.currentResults())
        self.assertEquals(4, len(results))
        
        self.assertEquals("X", results[0].getName())
        self.assertEquals("Y", results[1].getName())
        self.assertEquals("X", results[2].getName())
        self.assertEquals("X", results[3].getName())

    
class PosTest(unittest.TestCase):   
    def testValidateArgs(self):
        #test too many args, ie. more than 1
        args =["1","0"]
        try:
            Pos(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            #assertTrue(ifa.getMessage().contains("Pos takes exactly one argument."));
            pass
        
        
        #test with 1 argument, should be fine
        args = ["1"]
        try:
            Pos(args);
        except InvalidFunctionArguments, ifa:
            #self.assertTrue(ifa.getMessage().contains("The argument for Pos must be an integer >= 0"));
            pass
        
        
        #test with an argument of 0, should be fine
        args = ["0"]
        try:
            Pos(args);
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")

    def currentResults(self):
        x1 = XElement("X")
        x1.setAttributes({"position":"0"})
        
        x2 = XElement("X")
        x2.setAttributes({"position":"1"})
        
        x3 = XElement("X")
        x3.setAttributes({"position":"2"})
            
        y = XElement("Y")
        
        try:
            x1.setChildren([y])
        except:
            self.fail("Test will be thrown off because of this error!")
            
        return [x1, x2, x3]     
    
    def testEvaluate(self):
        #get position 0
        args = ["0"]
        pos = None
        try:
            pos = Pos(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")

        results = pos.evaluate(self.currentResults())
        self.assertEquals(1, len(results))
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("position"), "0")

        #get position 1
        args = ["1"]
        pos = None
        try:
            pos = Pos(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = pos.evaluate(self.currentResults())
        self.assertEquals(1, len(results))
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("position"), "1")

        #get position 2
        args = ["2"]
        pos = None
        try:
            pos = Pos(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = pos.evaluate(self.currentResults())
        self.assertEquals(1, len(results))
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("position"), "2")
        
	#get position 3, should get nothing back.
        args = ["3"]
        pos = None
        try:
            pos = Pos(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = pos.evaluate(self.currentResults())
        self.assertEquals(0, len(results))

        #test with current results as null
        args = ["3"]
        pos = None
        try:
            pos = Pos(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
		
        results = pos.evaluate(None)
        self.assertEquals(None, results);


class FirstTest(unittest.TestCase):
    def testValidateArgs(self):
        #test any arguments then an error should be thrown
        args = ["1"]
        try:
            First(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        
        #test with 0 argument, should be fine
        args = []
        try:
            First(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should not have been thrown by the constructor!")
            
        #test with null as arguments, should be fine
        args = None
        try:
            First(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should not have been thrown by the constructor!")

    def currentResults(self):
        x1 = XElement("X")
        x1.setAttributes({"position":"0"})
        x2 = XElement("X")
        x2.setAttributes({"position":"1"})
        x3 = XElement("X")
        x3.setAttributes({"position":"2"})
        y = XElement("Y")

        try:
            x1.setChildren([y])
        except:
            self.fail("Test will be thrown off because of this error!")

        return [x1, x2, x3]
        
    def testEvaluate(self):
        args = []
        first = None
        try:
            first = First(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
		
        results = first.evaluate(self.currentResults())
        self.assertEquals(1, len(results))
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("position"), "0")
        
        #same test as above but with null arguments
        args = None
        first = None
        try:
            first = First(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
		
        results = first.evaluate(self.currentResults());
        self.assertEquals(1, len(results))
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("position"), "0")
        

class HasAttributeTest(unittest.TestCase):
    def testValidateArgs(self):
        #test too many args, ie. more than 1
        args = ["name","bob","jones"]
        try:
            HasAttribute(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass

        #test with 2 argument, should fail
        args = ["name","bob","jones"]
        try:
            HasAttribute(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass

        #test with 0 argument, should be a problem
        args = []
        try:
            HasAttribute(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass

        #test with null arguments, should be a problem
        args = None
        try:
            HasAttribute(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass

        args = ["name"]
        try:
            HasAttribute(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should have NOT been thrown by the constructor!")


    def currentResults(self):
        x1 = XElement("X")
        x1.setAttributes({"number":"one", "pos":"0", "another":"testing1"})

        x2 = XElement("X")
        x2.setAttributes({"number":"two", "pos":"1"})

        x3 = XElement("X")
        x3.setAttributes({"number":"three", "pos":"2"})

        x4 = XElement("X")
        x4.setAttributes({"number":"one", "pos":"3", "another":"testing2"})

        x5 = XElement("X")
        x5.setAttributes({"number":"one", "pos":"4"})

        x6 = XElement("X")
        x6.setAttributes({"number":"one", "pos":"5"})

        y = XElement("Y");		
        try:
            x1.setChildren([y])
	except:
            self.fail("Test will be thrown off because of this error!")

        return [x1, x2, x3, x4, x5, x6]
    
    def testEvaluate(self):
        args = ["number"]
        ha = None
        try:
            ha = HasAttribute(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
		
        results = ha.evaluate(self.currentResults())
        self.assertEquals(6, len(results))

        for i in range(6):
            element = results[i]
            self.assertEquals("X", element.getName())
            self.assertEquals(element.getAttribute("pos"), "%d" % i)
        
        #doesn't exist in structure so, should get empty results
        args = ["truck"]
        ha = None
        
        try:
            ha = HasAttribute(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = ha.evaluate(self.currentResults())
        self.assertEquals(0, len(results))
        
        args = ["another"]
        ha = None
        try:
            ha = HasAttribute(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
		
        results = ha.evaluate(self.currentResults())
        self.assertEquals(2, len(results))
        
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("pos"), "0")
        self.assertEquals(element.getAttribute("another"), "testing1")
        
        element = results[1]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("pos"), "3")
        self.assertEquals(element.getAttribute("another"), "testing2")
    
class HasAttributeWithValueContainsTest(unittest.TestCase):
    def testValidateArgs(self):
        #test too many args, ie. more than 2
        args = ["name","bob","jones"]
        try:
            HasAttributeWithValueContains(args);
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
		
        #test with 1 argument, should fail
        args = ["name"]
        try:
            HasAttributeWithValueContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        		
        #test with 0 arguments, should be a problem
        args = []
        try:
            HasAttributeWithValueContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
		
        #test with null arguments, should be a problem
        args = None
        try:
            HasAttributeWithValueContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        
        #test with correct arguments, first one is zero, should work
        args = ["name","bob"]
        try:
            HasAttributeWithValueContains(args);
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should have NOT been thrown by the constructor!")


    def currentResults(self):
        x1 = XElement("X")
        x1.setAttributes({"number":"one", "pos":"0"})

        x2 = XElement("X")
        x2.setAttributes({"number":"two", "pos":"1"})

        x3 = XElement("X")
        x3.setAttributes({"number":"three", "pos":"2"})

        x4 = XElement("X")
        x4.setAttributes({"number":"one", "pos":"3"})

        x5 = XElement("X")
        x5.setAttributes({"number":"one", "pos":"4"})
        
        x6 = XElement("X")
        x6.setAttributes({"number":"one", "pos":"5"})

        y = XElement("Y")        
        try:
            x1.setChildren([y])
	except:
            self.fail("Test will be thrown off because of this error!")

        return [x1, x2, x3, x4, x5, x6]
                
    def testEvaluate(self):
        args = ["number", "ne"]
        hawvc = None
        try:
            hawvc = HasAttributeWithValueContains(args);
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = hawvc.evaluate(self.currentResults())
        self.assertEquals(4, len(results))
        
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("pos"), "0")
        
        element = results[1]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("pos"), "3")
        
        element = results[2]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("pos"), "4")
        
        element = results[3]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("pos"), "5")
        
        args = ["number", "two"]
        hawvc = None
        try:
            hawvc = HasAttributeWithValueContains(args);
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = hawvc.evaluate(self.currentResults())
        self.assertEquals(1, len(results))
        
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("pos"), "1")

class HasAttributeWithValueTest(unittest.TestCase):
    def testValidateArgs(self):
        #test too many args, ie. more than 2
        args = ["name","bob","jones"]
        try:
            HasAttributeWithValueContains(args);
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
		
        #test with 1 argument, should fail
        args = ["name"]
        try:
            HasAttributeWithValueContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        		
        #test with 0 arguments, should be a problem
        args = []
        try:
            HasAttributeWithValueContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
		
        #test with null arguments, should be a problem
        args = None
        try:
            HasAttributeWithValueContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        
        #test with correct arguments, first one is zero, should work
        args = ["name","bob"]
        try:
            HasAttributeWithValueContains(args);
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should have NOT been thrown by the constructor!")

    def currentResults(self):
        x1 = XElement("X")
        x1.setAttributes({"number":"one", "pos":"0"})

        x2 = XElement("X")
        x2.setAttributes({"number":"two", "pos":"1"})

        x3 = XElement("X")
        x3.setAttributes({"number":"three", "pos":"2"})

        x4 = XElement("X")
        x4.setAttributes({"number":"one", "pos":"3"})

        x5 = XElement("X")
        x5.setAttributes({"number":"one", "pos":"4"})
        
        x6 = XElement("X")
        x6.setAttributes({"number":"one", "pos":"5"})

        y = XElement("Y")        
        try:
            x1.setChildren([y])
	except:
            self.fail("Test will be thrown off because of this error!")

        return [x1, x2, x3, x4, x5, x6]

    def testEvaluate(self):
        args = ["number", "one"]
        hawv = None
        try:
            hawv = HasAttributeWithValueContains(args);
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = hawv.evaluate(self.currentResults())
        self.assertEquals(4, len(results))
        
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("pos"), "0")
        
        element = results[1]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("pos"), "3")
        
        element = results[2]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("pos"), "4")
        
        element = results[3]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("pos"), "5")
        
        args = ["number", "two"]
        hawv = None
        try:
            hawv = HasAttributeWithValueContains(args);
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = hawv.evaluate(self.currentResults())
        self.assertEquals(1, len(results))
        
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("pos"), "1")

class HasPCDataContainsTest(unittest.TestCase):
    def setUp(self):
        self.contains1 = "PCData"
        self.contains2 = "more PCData because I would like to test with more"

    def testValidateArgs(self):
        #test too many args, ie. more than 1
        args = ["name","bob","jones"]
        try:
            HasPCDataContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
		
        #test with 2 argument, should fail
        args = ["name", "position"]
        try:
            HasPCDataContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
		
        #test with 0 argument, should be a problem
        args = []
        try:
            HasPCDataContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        
        #test with null arguments, should be a problem
        args = None
        try:
            HasPCDataContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        
		
        #test with correct arguments, first one is zero, should work
        args = ["some text to look for in PCData"]
        try:
            HasPCDataContains(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should have NOT been thrown by the constructor!")

    def currentResults(self):
        x1 = XElement("X")
        x1.setAttributes({"position":"0"})
        
        x2 = XElement("X")
        x2.setAttributes({"position":"1"})
        
        x3 = XElement("X")
        x3.setAttributes({"position":"2"})

        y = XElement("Y")
        
        try:
            x1.setChildren([y])
            x1.setText("This is some test " + self.contains1 + ". I'm hoping that all of my tests go well." +
                       " They should, but until one actually runs the test you can never know.")
            x1.setText("This is the second " + self.contains1 + " Node that I'm adding to an element " +
                       "because I figure it gives me a better test.")
            x3.setText("This is some " + self.contains2 + " than " +
                       "one XElement containing a " + self.contains1 + " child")
            
        except:
           self.fail("Test will be thrown off because of this error!")

        return [x1, x2, x3]
    
    def testEvaluate(self):
        
        args = [self.contains1]
        hasPCDataContains = None
        try:
            hasPCDataContains = HasPCDataContains(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = hasPCDataContains.evaluate(self.currentResults())
        self.assertEquals(2, len(results))
        
        #self.assertTrue(results.get(0) instanceof XElement);
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("position"), "0")
        
        #assertTrue(results.get(0) instanceof XElement);
        element = results[1]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("position"), "2")
        
        #should get none in the results here
        args = ["The Zebras are not animatronic robots!"]
        hasPCDataContains = None
        try:
            hasPCDataContains = HasPCDataContains(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = hasPCDataContains.evaluate(self.currentResults())
        self.assertEquals(0, len(results))
        
        #should get one in the results
        args = [self.contains2]
        hasPCDataContains = None
        try:
            hasPCDataContains = HasPCDataContains(args);
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
    
        results = hasPCDataContains.evaluate(self.currentResults())
        self.assertEquals(1, len(results))
        
        #assertTrue(results.get(0) instanceof XElement);
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("position"), "2")
        

class HasPCDataTest(unittest.TestCase):
    def testValidateArgs(self):
        args = ["1"]
        try:
            HasPCData(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        
        args = ["1","test","bob"]
        try:
            HasPCData(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        
        #test with 0 argument, should be fine
        args = []
        try:
            HasPCData(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should not have been thrown.")
        
        #test with null as arguments, should be fine
        args = None 
        try:
            HasPCData(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should not have been thrown.")

    def currentResults(self):
        x1 = XElement("X")
        x1.setAttributes({"position":"0"})
        
        x2 = XElement("X")
        x2.setAttributes({"position":"1"})
        
        x3 = XElement("X")
        x3.setAttributes({"position":"2"})
        
        y = XElement("Y")
		
        try:
            x1.setChildren([y])
            x1.setText('''This is some test PCData. Im hoping that all of my tests go well.
                      They should, but until one actually runs the test you can never know''')
        
            x3.setText('''This is some more PCData because I would like to test with more than
                       one XElement containing a PCData child''')
            
        except:
            self.fail("Test will be thrown off because of this error!")

        return [x1, x2, x3]
                
    def testEvaluate(self):
        args = []
        hasPCData = None
        try:
            hasPCData = HasPCData(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
		
        results = hasPCData.evaluate(self.currentResults())
        self.assertEquals(2, len(results))
        
        #assertTrue(results.get(0) instanceof XElement);
        element = results[0]
        self.assertEquals("X", element.getName());
        self.assertEquals(element.getAttribute("position"), "0");
		
        #self.assertTrue(results.get(0) instanceof XElement);
        element = results[1]
        self.assertEquals("X", element.getName());
        self.assertEquals(element.getAttribute("position"), "2");

class LastTest(unittest.TestCase):
    def testValidateArgs(self):
        #test any arguments then an error should be thrown
        args = ["1"]
        try:
            Last(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        
        #test with 0 argument, should be fine
        args = []
        try:
            Last(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should not have been thrown by the constructor!")
        
        #test with null as arguments, should be fine
        args = None
        try:
            Last(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should not have been thrown by the constructor!")

    def currentResults(self):
        x1 = XElement("X")
        x1.setAttributes({"position":"0"})
        
        x2 = XElement("X")
        x2.setAttributes({"position":"1"})
        
        x3 = XElement("X")
        x3.setAttributes({"position":"2"})
        
        y = XElement("Y")
		
        try:
            x1.setChildren([y])
        except:
            self.fail("Test will be thrown off because of this error!")

        return [x1, x2, x3]
        
    def testEvaluate(self):
        args = []
        last = None
        try:
            last = Last(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!");
		
        results = last.evaluate(self.currentResults())
        self.assertEquals(1, len(results))
        
        #self.assertTrue(results.get(0) instanceof XNode);
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("position"), "2")
		
        #same test as above but with null arguments
        args = None
        try:
            last = Last(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!");
		
        results = last.evaluate(self.currentResults())
        self.assertEquals(1, len(results))
        
        #self.assertTrue(results.get(0) instanceof XNode);
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("position"), "2")

class PCDataContainsTest(unittest.TestCase):
    def setUp(self):
        self.contains1 = "PCData"
        self.contains2 = "more PCData because I would like to test with more"
        
    def testValidateArgs(self):
        #test too many args, ie. more than 1
        args = ["name","bob","jones"]
        try:
            PCDataContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
		
        #test with 2 argument, should fail
        args = ["name","bob"]
        try:
            PCDataContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        
        #test with 0 argument, should be a problem
        args = []
        try:
            PCDataContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        
        #test with null arguments, should be a problem
        args = None
        try:
            PCDataContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        
        #test with correct arguments, first one is zero, should work
        args = ["some text to look for in PCData"]
        try:
            PCDataContains(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
            
    def currentResults(self):
        x1 = XElement("X")
        x1.setAttributes({"position":"0"})
        
        x2 = XElement("X")
        x2.setAttributes({"position":"1"})
        
        x3 = XElement("X")
        x3.setAttributes({"position":"2"})

        y = XElement("Y")
        
        try:
            x1.setChildren([y])
            x1.setText("This is some test " + self.contains1 + ". I'm hoping that all of my tests go well." +
                       " They should, but until one actually runs the test you can never know.")
            x1.setText("This is the second " + self.contains1 + " Node that I'm adding to an element " +
                       "because I figure it gives me a better test.")
            x3.setText("This is some " + self.contains2 + " than " +
                       "one XElement containing a " + self.contains1 + " child")
            
        except:
           self.fail("Test will be thrown off because of this error!")

        return [x1, x2, x3]
    
    def testEvaluate(self):
        args = [self.contains1]
        pcDataContains = None
        try:
            pcDataContains = PCDataContains(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = pcDataContains.evaluate(self.currentResults())
        #check this
        self.assertEquals(2, len(results))
        
        #assertTrue(results.get(0) instanceof XPCData)
        pcdata = results[0]
        self.assertTrue(pcdata.__contains__(self.contains1))
        
        #should get none in the results here
        args = ["The Zebras are not animatronic robots!"]
        pcDataContains = None
        try:
            pcDataContains = PCDataContains(args)
        except InvalidFunctionArguements, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
		
        results = pcDataContains.evaluate(self.currentResults())
        self.assertEquals(0, len(results))
        
        #should get one in the results
        args = [self.contains2]
        pcDataContains = None
        try:
            pcDataContains = PCDataContains(args)
        except InvalidFunctionArguements, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
		
        results = pcDataContains.evaluate(self.currentResults())
        self.assertEquals(1, len(results))
        
        #self.assertTrue(results.get(0) instanceof XPCData)
        pcdata = results[0]
        self.assertTrue(pcdata.__contains__(self.contains2))
		

class PCDataTest(unittest.TestCase):

    def setUp(self):
	self.pcdata1 = '''This is some test PCData. I'm hoping that all 
        of my tests go well. They should, but until one actually runs the
        test you can never know'''
	
	self.pcdata2 = '''This is the second PCData Node that I'm adding to an element 
        because I figure it gives me a better test.'''
	
	self.pcdata3 = '''This is some more PCData because I would like to
        test with more than one XElement containing a PCData child'''
    
    def testValidateArgs(self):
        #test any arguments then an error should be thrown
        args = ["1"]
        try:
            Last(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        
        #test with 0 argument, should be fine
        args = []
        try:
            Last(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should not have been thrown by the constructor!")
        
        #test with null as arguments, should be fine
        args = None
        try:
            Last(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should not have been thrown by the constructor!")


    def currentResults(self):
        x1 = XElement("X")
        x1.setAttributes({"position":"0"})
        
        x2 = XElement("X")
        x2.setAttributes({"position":"1"})
        
        x3 = XElement("X")
        x3.setAttributes({"position":"2"})
        
        y = XElement("Y")
		
        try:
            x1.setText(self.pcdata1+self.pcdata2)
            x3.setText(self.pcdata3)
            x1.setChildren([y])
        except:
            self.fail("Test will be thrown off because of this error!")

        return [x1, x2, x3]
                    
    def testEvaluate(self):
        args = []
        pcData = None
        try:
            pcData = PCData(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = pcData.evaluate(self.currentResults())
        self.assertEquals(3, len(results))
        
        #self.assertTrue(results.get(0) instanceof XPCData)
        text = results[0]
        self.assertTrue(text == self.pcdata1 + self.pcdata2)

        text = results[2]
        self.assertTrue(text == self.pcdata3)
    
class RangeTest(unittest.TestCase):
    def testValidateArgs(self):
                #test too many args, ie. more than 2
        args = ["name","bob","jones"]
        try:
            HasAttributeWithValueContains(args);
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
		
        #test with 1 argument, should fail
        args = ["name"]
        try:
            HasAttributeWithValueContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        		
        #test with 0 arguments, should be a problem
        args = []
        try:
            HasAttributeWithValueContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
		
        #test with null arguments, should be a problem
        args = None
        try:
            HasAttributeWithValueContains(args)
            self.fail("An InvalidFunctionArguements exception should have been thrown by the constructor!")
        except InvalidFunctionArguments, ifa:
            pass
        
        #test with correct arguments, first one is zero, should work
        args = ["name","bob"]
        try:
            HasAttributeWithValueContains(args);
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguements exception should have NOT been thrown by the constructor!")


    def currentResults(self):
        x1 = XElement("X")
        x1.setAttributes({"position":"0"})
        
        x2 = XElement("X")
        x2.setAttributes({"position":"1"})
        
        x3 = XElement("X")
        x3.setAttributes({"position":"2"})
        
        x4 = XElement("X")
        x4.setAttributes({"position":"3"})
        
        x5 = XElement("X")
        x5.setAttributes({"position":"4"})

        x6 = XElement("X")
        x6.setAttributes({"position":"5"})
        
        
        y = XElement("Y")
        try:
            x1.setChildren([y])
        except:
            self.fail("Test will be thrown off because of this error!")
    
        return [x1, x2, x3, x4, x5]
            
    def testEvaluate(self):
        args = ["0", "3"]
        myRange = None
        try:
            myRange = Range(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = myRange.evaluate(self.currentResults())
        self.assertEquals(3, len(results))

        x = 0
        for element in results:
            self.assertEquals("X", element.getName())
            self.assertEquals(element.getAttribute("position"), "%d" % x)
            x+=1		
	
        args = ["1", "2"]
        myRange = None
        try:
            myRange = Range(args)
        except InvalidFunctionArguments, ifa:
            self.fail("An InvalidFunctionArguments exception should not have been thrown!")
        
        results = myRange.evaluate(self.currentResults())
        self.assertEquals(1, len(results))
        element = results[0]
        self.assertEquals("X", element.getName())
        self.assertEquals(element.getAttribute("position"), "1")	

if __name__ == '__main__':
    unittest.main()
