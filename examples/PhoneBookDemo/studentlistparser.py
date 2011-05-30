import sys
import os
import os.path
from xparser import XElementParser
from xelement import XElement

class Students(XElement):
   def printMyStudents(self):
      print '-- Your Students --'
      for student in self.getChildren(Student):
          student.printStudentInfo()
      print '--------------------'

class Student(XElement): 
   def printStudentInfo(self):
      attrs = self.getAttributes()
      print attrs.getFirst('code_name'), attrs.getFirst('student_id'), attrs.getFirst('name'), self.getText()

class MyPhoneBook:
   def __init__(self, students):
      self.pb = {}
      for student in students:
         if student.hasAttributes(['code_name','student_id', 'name']):
            self.pb[student.getAttributes().getFirst('nick_name')] = student
         else:
            exc = "malformed entry in your phone book:\n %s" % student.toXML()
            raise str(exc)

   def lookup(self, nick_name):
      try:
         return self.pb[nick_name].getAttributes().getFirst('number')
      except:
         return None



if len(sys.argv) < 3:
   print "usage: phonebook.py phonebook.xml code_name"
   sys.exit(1)

my_classes = { 'Students':Students, 'Student':Student }
xparser = XElementParser(my_classes)
doc = xparser.process(sys.argv[1])
doc.printMyStudents()
pb = MyPhoneBook(doc.getChildren(Student))
print sys.argv[2], pb.lookup(sys.argv[2])
