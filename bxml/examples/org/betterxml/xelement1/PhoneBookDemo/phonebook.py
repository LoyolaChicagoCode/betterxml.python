"""
XIR Toolkit
Copyright (c) 2003 by Nimkathana Corporation
Licensed under the LGPL (included with the source code)

        Source: $Id: phonebook.py,v 1.1 2006/07/16 22:22:09 gkt Exp $

    Revised by: $Author: gkt $

 Revision date: $Date: 2006/07/16 22:22:09 $

"""
import sys
import os
import os.path


sys.path.append('../../../../../src')

from org.betterxml.xelement1.xparser import XElementParser
from org.betterxml.xelement1.xelement import XElement

class Friends(XElement):
   def printMyFriends(self):
      print '-- Your Phonebook --'
      for friend in self.getChildren(Friend):
          friend.printFriendInfo()
      print '--------------------'

class Friend(XElement): 
   def printFriendInfo(self):
      attrs = self.getAttributes()
      print attrs.getFirst('nick_name'), attrs.getFirst('number'), self.getText()

class MyPhoneBook:
   def __init__(self, friends):
      self.pb = {}
      for friend in friends:
         if friend.hasAttributes(['nick_name','number']):
            self.pb[friend.getAttributes().getFirst('nick_name')] = friend
         else:
            exc = "malformed entry in your phone book:\n %s" % friend.toXML()
            raise str(exc)

   def lookup(self, nick_name):
      try:
         return self.pb[nick_name].getAttributes().getFirst('number')
      except:
         return None


def go(filename, code_name):
   my_classes = { 'Friends':Friends, 'Friend':Friend }
   xparser = XElementParser(my_classes)
   doc = xparser.process(filename)
   doc.printMyFriends()
   pb = MyPhoneBook(doc.getChildren(Friend))
   print code_name, pb.lookup(code_name)
   return doc

if __name__ == '__main__':
   if len(sys.argv) < 3:
      print "usage: phonebook.py phonebook.xml code_name"
      sys.exit(1)
   filename = sys.argv[1]
   code_name = sys.argv[2]
   go(filename, code_name)
