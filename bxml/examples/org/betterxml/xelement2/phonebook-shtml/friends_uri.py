import sys
import os
import os.path

sys.path.append('../../..')

from org.betterxml.xelement2.xelement2 import XElement

def getNamespaceURI():
   return "http://mydomain.com/friends"

def getDefaultElementClass():
   return XElement

def getMappings():
   return { 'Friends' : Friends, 'Friend' : Friend }

class Friends(XElement):
   def printMyFriends(self):
      print '-- Your Phonebook --'
      for friend in self.getChildren(Friend):
          friend.printFriendInfo()
      print '--------------------'

class Friend(XElement): 
   def printFriendInfo(self):
      attrs = self.getAttributes()
      print attrs.getByName('nick_name'), attrs.getByName('number'), self.getText()
