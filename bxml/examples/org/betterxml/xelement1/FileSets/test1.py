"""
XIR Toolkit
Copyright (c) 2003 by Nimkathana Corporation
Licensed under the LGPL (included with the source code)

        Source: $Id: test1.py,v 1.1 2006/07/16 22:22:07 gkt Exp $

    Revised by: $Author: gkt $

 Revision date: $Date: 2006/07/16 22:22:07 $

"""
#!/usr/bin/env python

import os
import os.path

from FileSet import FileSet

def test1():
   test_fileset = os.path.join(os.getcwd(), 'fileset1')
   fs = FileSet(test_fileset)
   fs.next_run()
   fs.new_context('compute')
   fs.next_iter()
   fs.new_dataset('alpha')
   fs.new_dataset('beta')
   fs.next_iter()
   fs.new_dataset('alpha')
   fs.new_dataset('beta')
   fs.commit()

def test2():
   test_fileset = os.path.join(os.getcwd(), 'fileset2')
   fs = FileSet(test_fileset)
   fs.next_run()
   test_data = range(0,10)

   fs.new_context('rotate')
   for i in range(0, 20):
      fs.next_iter()
      filename = fs.new_dataset('my_list')
      print filename
      fp = open(filename, 'w')
      for x in test_data:
         fp.write("%d\n" % x)
      test_data = test_data[1:] + test_data[0:1]
      fp.close()

   fs.commit()

if __name__ == '__main__':
   test2()
