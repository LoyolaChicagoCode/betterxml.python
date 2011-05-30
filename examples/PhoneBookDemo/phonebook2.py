import sys
import os
import os.path
from xparser import XElementParser
from xelement import XElement

class Friends(XElement):
   def initialize(self):
      self.pb = {}

   def finalize(self, parent):
      for friend in self.getChildren(Friend):
         if friend.hasAttributes(['nick_name','number']):
            self.pb[friend.getAttributes().getFirst('nick_name')] = friend
         else:
            print "malformed entry in phonebook",friend.toXML()

   def lookup_nick_name(self, nick_name):
      return self.pb[nick_name].toXML(prologue="")

   def printMyFriends(self):
      print '-- Your Phonebook --'
      for friend in self.getChildren(Friend):
          friend.printFriendInfo()
      print '--------------------'

class Friend(XElement): 
   def printFriendInfo(self):
      attrs = self.getAttributes()
      print attrs.getFirst('nick_name'), attrs.getFirst('number'), self.getText()


def go(filename, nick_name):
   my_classes = { 'Friends':Friends, 'Friend':Friend }
   xparser = XElementParser(my_classes)
   doc = xparser.process(filename)
   doc.printMyFriends()
   print doc.lookup_nick_name(nick_name)

if __name__ == '__main__':
   if len(sys.argv) < 3:
      print "usage: phonebook.py phonebook.xml nick_name"
      sys.exit(1)
   filename = sys.argv[1]
   nick_name = sys.argv[2]
   go(filename, nick_name)
