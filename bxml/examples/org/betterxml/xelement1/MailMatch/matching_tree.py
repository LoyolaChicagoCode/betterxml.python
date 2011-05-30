"""
XIR Toolkit
Copyright (c) 2003 by Nimkathana Corporation
Licensed under the LGPL (included with the source code)

        Source: $Id: matching_tree.py,v 1.1 2006/07/16 22:22:08 gkt Exp $

    Revised by: $Author: gkt $

 Revision date: $Date: 2006/07/16 22:22:08 $

"""
import sys
import os
import os.path
import string
import re

sys.path.append('../../../../../src')

from org.betterxml.xelement1.xparser import XElementParser
from org.betterxml.xelement1.xelement import XElement

class Message:
   def __init__(self, to_list, from_list, subject, etc):
      if type(to_list) == type(''):
	 self.to_list = string.split(to_list,",")
      elif type(to_list) == type([]):
	 self.to_list = to_list
      else:
         raise "to_list must be string or list"

      if type(from_list) == type(''):
	 self.from_list = string.split(from_list,",")
      elif type(from_list) == type([]):
	 self.from_list = from_list
      else:
         raise "from_list must be string or list"

      if type(subject) == type(''):
         self.subject = subject
      else:
         raise "subject must be a string"
          
      if type(etc) == type({}):
         self.etc = etc
      else:
         raise "etc must be a dictionary (the message content)"

   def match_to(self, expr):
      for entry in self.to_list:
         if expr.match(entry): 
            return 1
      return 0

   def match_from(self, expr):
      for entry in self.from_list:
         if expr.match(entry): 
            return 1
      return 0

   def match_subject(self, expr):
      if expr.match(self.subject):
         return 1
      return 0

class MatchCommon(XElement):
   def initialize(self):
      self.match_expr_text = self.getAttributes().getFirst('match')
      self.match_expr = re.compile(self.match_expr_text)

   def get_match_regex(self):
      return self.match_expr

   def match(self, message):
      raise "must override in subclass"

class To(MatchCommon):
   def match(self, message):
      return message.match_to(self.get_match_regex())

class From(MatchCommon):
   def match(self, message):
      return message.match_from(self.get_match_regex())
   
class Subject(MatchCommon):
   def match(self, message):
      return message.match_subject(self.get_match_regex())

class And(MatchCommon):
   def initialize(self):
      pass

   def match(self, message):
      for child in self.getChildren():
          if not child.match(message):
	     return 0
      return 1

class Or(MatchCommon):
   def initialize(self):
      pass

   def match(self, message):
      for child in self.getChildren():
          if child.match(message):
	     return 1
      return 0

class Rule(MatchCommon):
   def initialize(self):
      pass

   def match(self, message):
      return self.getChildren()[0].match(message)

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



if len(sys.argv) < 2:
   print "usage: matching_tree.py rule.xml"
   sys.exit(1)

my_classes = { 'To' : To, 'From' : From, 'Subject' : Subject,
	       'And' : And, 'Or' : Or, 'Rule' : Rule }

msg1 = Message('gkt@cs.luc.edu','gkt@acm.org', 'Hello World', {})
msg2 = Message('nina@quillscape.com','gkt@acm.org', 'Hello World 2', {})
msg3 = Message('abc@def.org,ghi@jkl.org','nina@quillscape.com', 'Hello World 3', {})
msg4 = Message('abc@def.org,ghi@jkl.org','nina@quillscape.com', 'Goodbye World 3', {})

xparser = XElementParser(my_classes)
try:
  doc = xparser.process(sys.argv[1])
except:
  print "Due to above errors, I am bailing out!"
  sys.exit(1)

print doc.toXML()
print "msg1",doc.match(msg1)
print "msg2",doc.match(msg2)
print "msg3",doc.match(msg3)
print "msg4",doc.match(msg4)

#pb = MyPhoneBook(doc.getChildren(Friend))
#print sys.argv[2], pb.lookup(sys.argv[2])
