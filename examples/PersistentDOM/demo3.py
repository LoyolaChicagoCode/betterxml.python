#!/usr/local/python-2.1/bin/python

from PXML import PElement

"""
If you have run demo1.py, you can run this to see the tree that was created
"""

def test1():

   # This creates an XML document based in subdirectory 'xyz'
   e = PElement('xyz')
   print e.get_element_count()
   e = e.get_element(0)
   for i in range(0,e.get_element_count()):
      child = e.get_element(i)
      if child.get_name() == 'y':
         count = child.get_first_attribute('count')
         print "count = %s" % count
         if count == None:
            child.add_attribute('count', 0)
            print "could not find 'count' attribute in a y; one has been added"
            continue
         count = int(count) + 1
         child.change_attribute('count', count)

   print "after updating counts in y's attributes"

   print e.toXML()

test1()
