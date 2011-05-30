import unittest
import sys

sys.path.append('../../../../src/')

from org.betterxml.xelement1.xattributes import XAttributes

class TestXAttributes(unittest.TestCase):
	
    def setUp(self):
        self.d = {'key1':'value1','key2':'value2','key3':'value3'}
        self.xattrs = XAttributes(self.d)


    def testcontainsAttribute(self):
        #test not containing, should return 0 (false)
        self.assertEqual(0, self.xattrs.containsAttribute("key4"))
        self.assertEqual(0, self.xattrs.containsAttribute("value1"))
        self.assertEqual(0, self.xattrs.containsAttribute("value"))
        
        #test containing, should return 1 (true)
        self.assertEqual(1, self.xattrs.containsAttribute("key1"))
        self.assertEqual(1, self.xattrs.containsAttribute("key2"))
        self.assertEqual(1, self.xattrs.containsAttribute("key3"))


    def testcontainsAttributes(self):
        #test not containing any of them, should return 0 (false)
        l = ["abcd","key","key4","value"]
        self.assertEqual(0, self.xattrs.containsAttributes(l))

        #test contains all but one of them, should return 0 (false)
        l = ["key1","key2","key3","key4"]
        self.assertEqual(0, self.xattrs.containsAttributes(l))
        
        #test contains all of them, should return 1 (true)
        l = ["key1","key2","key3"]
        self.assertEqual(1, self.xattrs.containsAttributes(l))
        
        #empty list, should return 1 (true)
        l = []
        self.assertEqual(1, self.xattrs.containsAttributes(l))


    def testgetAttributes(self):
        d2 = self.xattrs.getAttributes()
        self.assertEqual(self.d, d2)

        self.xattrs.setAttribute("key4", "value4")
        d3 = self.xattrs.getAttributes()
        self.assertNotEqual(d3, self.d)
        self.assertEqual(4, len(d3))


    def testgetAttributeValue(self):
        #first, should be notEqual
        self.assertNotEqual("blah", self.xattrs.getAttributeValue("key1"))
        self.assertNotEqual("value", self.xattrs.getAttributeValue("key1"))

        #should be equal because key does not exist
        self.assertEqual(None, self.xattrs.getAttributeValue("key7"))

        #these should all work because they are there and right
        self.assertEqual("value1", self.xattrs.getAttributeValue("key1"))
        self.assertEqual("value2", self.xattrs.getAttributeValue("key2"))
        self.assertEqual("value3", self.xattrs.getAttributeValue("key3"))


    def testremoveAttribute(self):
        self.assertEqual(1, self.xattrs.containsAttribute("key1"))
        self.assertEqual(3, self.xattrs.size())
        self.xattrs.removeAttribute("key1")
        self.assertEquals(0, self.xattrs.containsAttribute("key1"))
        self.assertEqual(2, self.xattrs.size())

        #try removing something that isn't there. this shouldn't be a problem
        self.assertEqual(2, self.xattrs.size())
        self.xattrs.removeAttribute("key5")
        self.assertEqual(2, self.xattrs.size())

    def testsetAttribute(self):
        #set a new attribute
        self.assertEquals(None, self.xattrs.getAttributeValue("key4"))
        self.xattrs.setAttribute("key4", "value4")
        self.assertEquals("value4", self.xattrs.getAttributeValue("key4"))

        #set one that is already set
        self.assertEquals("value1", self.xattrs.getAttributeValue("key1"))
        self.xattrs.setAttribute("key1", "new value1")
        self.assertEquals("new value1", self.xattrs.getAttributeValue("key1"))


    def testsize(self):
        self.assertEqual(3, self.xattrs.size())
        self.assertNotEqual(4, self.xattrs.size())
        self.assertNotEqual(2, self.xattrs.size())


    def testtoXML(self):
        #try if no attributes
        noAttrs = XAttributes()
        self.assertEqual("", noAttrs.toXML())
        
        #can't really test anything else because the order we get
        # the attributes in from the dictionary is not predictable
        # so we can't build a string and compare them (and I'm too 
        # lazy to do any kind of regex testing or series of string 
        # searches.


if __name__ == '__main__':
    unittest.main()