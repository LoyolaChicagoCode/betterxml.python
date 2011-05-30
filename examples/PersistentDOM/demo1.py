#!/usr/local/python-2.1/bin/python
from PXML import PElement

"""
We'll be encoding a test document:
<x x1="x1" x2="x2>
  <y y1="y1">
     one
  </y>
  <y y2="y2">
     two
  </y>
  three
</x>
"""

def test1():

   # This creates an XML document based in subdirectory 'xyz'
   e = PElement('xyz')

   # set the element's name and add 3 sub-elements (2 elements, 1 cdata)
   # name the element 'x'
   e.set_name('x')
   e.add_element(2)
   e.add_cdata_element()

   # set the attributes of element 'x'
   e.add_attribute('x1','x1')
   e.add_attribute('x2','x2')

   # now let's setup the first 'y' element 
   y1 = e.get_element(-3)
   y1.set_name('y')
   y1.add_attribute('y1','y1')
   y1.add_attribute('count','0')
   y1.add_cdata_element()
   y1text = y1.get_element(0)
   y1text.set_text('one')


   # now let's setup the second 'y' element
   y2 = e.get_element(-2)
   y2.set_name('y')
   y2.add_attribute('y2','y2')
   y2.add_attribute('count','0')
   y2.add_cdata_element()
   y2text = y2.get_element(0)
   y2text.set_text('two')

   # and the text element following the two y's
   etext = e.get_element(-1)
   etext.set_text('three')

   print e.toXML()

test1()
