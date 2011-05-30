import unittest

class TestList(unittest.TestCase):

   def setUp(self):
      self.myList = []

   def testAppend1(self):
      self.myList.append(1)
      assert len(self.myList) == 1 and self.myList[-1] == 1

   def testAppendN(self):
      items = 1000
      for i in range(1, items+1):
         self.myList.append(i)
      assert len(self.myList) == items and sum(self.myList) == items * (items + 1)/2

   def testLength0(self):
      assert len(self.myList) == 0

unittest.main()
