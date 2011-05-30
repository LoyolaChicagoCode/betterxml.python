import sys
import os
import os.path

sys.path.append('../..')
sys.path.append('../../..')

from org.betterxml.xelement2.xparser import XElementParser

import friends_uri
import shtml_uri

class MyPhoneBook:
   def __init__(self, friends):
      self.pb = {}
      for friend in friends:
         #if friend.hasAttributes(['nick_name','number']):
         self.pb[friend.getAttributes().getByName('nick_name')] = friend
         #else:
         #   exc = "malformed entry in your phone book:\n %s" % friend.toXML()
         #   raise str(exc)

   def lookup(self, nick_name):
      try:
         return self.pb[nick_name].getAttributes().getByName('number')
      except:
         return None


def go(filename, code_name):
   # The list must contain a module for each XML namespace to be parsed!
   xparser = XElementParser([friends_uri, shtml_uri])
   doc = xparser.process(filename)
   print "document is",doc
   doc.printMyFriends()
   pb = MyPhoneBook(doc.getChildren(friends_uri.Friend))
   print code_name, pb.lookup(code_name)
   return doc

if __name__ == '__main__':
   if len(sys.argv) < 3:
      print "usage: phonebook.py phonebook.xml code_name"
      sys.exit(1)
   filename = sys.argv[1]
   code_name = sys.argv[2]
   go(filename, code_name)
