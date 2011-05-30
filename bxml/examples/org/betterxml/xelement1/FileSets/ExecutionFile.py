"""
XIR Toolkit
Copyright (c) 2003 by Nimkathana Corporation
Licensed under the LGPL (included with the source code)

        Source: $Id: ExecutionFile.py,v 1.1 2006/07/16 22:22:07 gkt Exp $

    Revised by: $Author: gkt $

 Revision date: $Date: 2006/07/16 22:22:07 $

"""
#!/usr/local/python-2.0.1/bin/python
# Standard Python import

import string
import sys
import types
import os
import time

# Python XML Support for SAX

from xml.sax import saxexts
from xml.sax import saxlib

# George's XElement framework for simple XML tree processing

from xelement import XElement, XTreeHandler, CreateElement
import BootstrapMetadata

# These are tree node classes. They are merely placeholders so we can select
# nodes using XElement's getChild() and getChildren() methods, which allow
# you to specify the type of node to be extracted. You can see how this
# is done by studying the nextRun() method.

class Execution(XElement):
   def getMaxRun(self):
      run_list = self.getChildren(Run)
      if not run_list:
         return None
      max_run_id = run_list[0].getAttributes().getFirst('id')
      max_run_id = int(max_run_id)
      for r in run_list[1:]:
         run_id = r.getAttributes().getFirst('id')
         run_id = int(run_id)
         if run_id > max_run_id:
            max_run_id = int(run_id)
      return max_run_id
    
   def getRun(self, id):
      for r in self.getChildren(Run):
          run_id = int(r.getAttributes().getFirst('id'))
          if run_id == id:
             return r
      return None

   def nextRun(self, metadata_dir):
      run_list = self.getChildren(Run)
      local_time = time.localtime(time.time())
      todays_date = time.strftime('%m-%d-%Y', local_time)
      todays_time = time.strftime('%H.%M.%S', local_time)
      max_run_id = self.getMaxRun()
      if max_run_id == None:
         max_run_id = 0
      next_run_id = max_run_id + 1
      rf_name = os.path.join(metadata_dir, 'Run%s.xml')
      rf_name = rf_name % (next_run_id)
      if not os.path.exists(rf_name):
         fp = open(rf_name, 'w')
         fp.write(BootstrapMetadata.RUN_FILE % (next_run_id))
         fp.close()

      new_run = CreateElement(name='Run',
                              attributes=[('id',next_run_id),
                                          ('date', todays_date),
                                          ('time', todays_time),
                                          ('run_file', rf_name)])
      self.linkTo(new_run)
      return new_run

   def currentRun(self):
      run_id = self.getMaxRunId()
      if run_id == None:
         raise "There is no current run."
      return self.getRun(run_id)
      


class Run(XElement): pass

class ExecutionFile:
   RUNFILE_NAME_TEMPLATE = "%s/.md/Run%d.xml"

   def __init__(self, filename, fileset=".", **kw):
      self.xth = XTreeHandler(IgnoreWhiteSpace='yes', 
                              RemoveWhiteSpace='yes', CreateElementMap='yes')
      self.xth.registerElementClass(Execution)
      self.xth.registerElementClass(Run)
      try:
         self.saxp = kw['sax_parser']
      except:
         self.saxp = saxexts.make_parser()
      self.saxp.setDocumentHandler(self.xth)
      self.filename = filename
      self.fileset = fileset
      self.execution = None
      self.backup_on_change = kw.get('backups', 1)

   def __requires_execution(self):
      if self.execution == None:
         raise "you must either load() a file or start building a document"

   def getExecution(self):
      self.__requires_execution()
      return self.execution

   def load(self):
      Ok=None
      try:
         self.saxp.parse(self.filename)
         document = self.xth.getDocument()
         print "document %s" % document
         print document.children[0].__class__.__name__
         self.execution = document.getChild(Execution)
         print type(self.execution)
      except IOError,e:
         print "could not load or read %s" % self.filename
      except saxlib.SAXException,e:
         print "SAX Parser error %s " % e
      print "load success"

   def save(self):
      self.__requires_execution()
      local_time = time.localtime(time.time())
      if self.backup_on_change:
         todays_date = time.strftime('%m-%d-%Y', local_time)
         todays_time = time.strftime('%H.%M.%S', local_time)
         backup_filename = self.filename + '_' + todays_date + '_' + todays_time
         os.system('/bin/cp %s %s' % (self.filename, backup_filename))
      executionAsXML = self.execution.toXML()
      fp = open(self.filename, 'w')
      fp.write(executionAsXML)
      fp.close()

   
def test1(filename='.md/Executions.xml'):
   rf = ExecutionFile(filename)

   rf.load()
   r = rf.execution.nextRun()
   rf.save()
   print "run count = %s" % r.getAttributes().getFirst('id')

new_run = test1

def test2(filename='.md/Executions.xml'):
   p = saxexts.make_parser()

   print "Beginning performance tests"
   for psize in [10, 100]:
      t1 = time.time()
      for i in range(0, psize):
         rf = ExecutionFile(filename)
         rf.load()
         rf.execution.nextRun()
         rf.save()
      t2 = time.time()
      print "files written %d in %d seconds" % (psize, t2-t1)

def test3(filename='.md/Executions.xml'):
   ef = ExecutionFile(filename)
   ef.load()
   print "current run id = %d" % ef.execution.getMaxRun()
   r = ef.execution.getRun(ef.execution.getMaxRun())
   from RunFile import RunFile
   rf_name = r.getAttributes().getFirst('run_file')
   print "current run's file is %s" % rf_name
   rf = RunFile(rf_name, sax_parser = ef.saxp)
   rf.load()
   try:
      cl_context = rf.run.createContext('compute_loop')
      cl_context = rf.run.getContext('compute_loop')
   except:
      cl_context = rf.run.getContext('compute_loop')

   iter1 = cl_context.nextIteration()
   print "current iteration  = %s" % iter1.getAttributes().getFirst('count')
   iter1.createDataSet('rho', 'compute', 'enzo')
   iter1.createDataSet('rho_jpeg', 'render', 'enzo')
   print "saving metadata"
   rf.save()

next_iteration = test3

if __name__ == '__main__':
   if len(sys.argv) < 2:
      print "usage: ExecutionFile [new_run | next_iteration]"
      sys.exit(1)
   method = vars()[sys.argv[1]]
   method()
