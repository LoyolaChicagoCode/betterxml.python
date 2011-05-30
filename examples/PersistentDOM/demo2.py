#!/usr/local/python-2.1/bin/python
from PXML import PElement

"""
If you have run demo1.py, you can run this to see the tree that was created
"""

def test1():

   # This creates an XML document based in subdirectory 'xyz'
   e = PElement('xyz')
   print e.toXML()

test1()
