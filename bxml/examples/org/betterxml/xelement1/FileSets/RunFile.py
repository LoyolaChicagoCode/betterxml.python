"""
XIR Toolkit
Copyright (c) 2003 by Nimkathana Corporation
Licensed under the LGPL (included with the source code)

        Source: $Id: RunFile.py,v 1.1 2006/07/16 22:22:07 gkt Exp $

    Revised by: $Author: gkt $

 Revision date: $Date: 2006/07/16 22:22:07 $

"""
# Standard Python imports

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

class Run(XElement):
   def __init__(self):
      XElement.__init__(self)

   def getContext(self,name):
      context_list = self.getChildren(Context)
      for c in context_list:
          if c.getAttributes().getFirst('name') == name:
             return c
      return None

   def createContext(self,name):
      if self.getContext(name) != None:
         raise "context %s already exists" % str(name)
      new_context = CreateElement(element_class=Context,
                                  name='Context',
                                  attributes=[('name', name)])
      self.linkTo(new_context)
      return new_context
      
   def getAllContexts(self):
      return self.getChildren(Context)

class Context(XElement):
   def __init__(self):
      self.last_iteration = None
      XElement.__init__(self)

   def nextIteration(self, user_index_name=None, user_index_value=None):
      if self.last_iteration == None:
         count = 0
      else: 
         count = self.last_iteration + 1

      if user_index_name == None:
         new_iter = CreateElement(element_class=Iteration,
                                  name='Iteration',
                                  attributes=[('count', count)])
      else:
         new_iter = CreateElement(element_class=Iteration,
                                 name='Iteration',
                                 attributes=[('user_index_name',user_index_name),
                                        ('user_index_value',user_index_value),
                                        ('count', count)])
      self.linkTo(new_iter)
      self.last_iteration = count
      return new_iter

   def getIterations(self):
      return self.getChildren(Iteration)

   def initialize(self):
      self.last_iteration = None

   def finalize(self, parent):
      all_iterations = self.getChildren(Iteration)
      self.last_iteration = None
      for i in all_iterations:
         count = i.getAttributes().getFirst('count')
         if self.last_iteration == None or count > self.last_iteration:
            self.last_iteration = int(count)

class Iteration(XElement):
   def __init__(self):
      XElement.__init__(self)

   def getDataSet(self, name, phase):
      dataset_list = self.getChildren(DataSet)
      for ds in dataset_list:
         ds_name = ds.getAttributes().getFirst('name')
         ds_phase = ds.getAttributes().getFirst('phase')
         if ds_name == name and ds_phase == phase:
            return ds
      return None 

   def createDataSet(self, name, phase, run_id):
      my_count = self.attrs.getFirst('count')
      if self.getDataSet(name, phase) != None:
         raise "Data set %s was already created in phase %s iteration %s" % (name, phase, my_count)
      interp_dict = {
         'phase' : phase, 'iter' : my_count, 'name' : name, 'run_id' : run_id
      }
      new_dataset_filename = '.d/phase_%(phase)s.iteration_%(iter)s.name_%(name)s.run_%(run_id)s'
      new_dataset_filename =  new_dataset_filename % interp_dict
      new_dataset = CreateElement(element_class=DataSet, name='DataSet',
                                  attributes=[('name', name), ('phase', phase),
                                          ('file_name', new_dataset_filename)])
      self.linkTo(new_dataset)
      return new_dataset_filename

   def getDataSet(self, name, phase):
      for ds in self.getChildren(DataSet):
         ds_name = ds.getAttributes().getFirst('name')
         ds_phase = ds.getAttributes().getFirst('phase')
         if ds_name == name and ds_phase == phase:
            return ds
      return None

   
class DataSet(XElement):
   def __init__(self):
      XElement.__init__(self)

   def getName(self):
      return self.attrs.getFirst('name')

   def getPhase(self):
      return self.attrs.getFirst('phase')

   def getFileName(self):
      return self.attrs.getFirst('file_name')

class RunFile:
   def __init__(self, filename, **kw):
      self.xth = XTreeHandler(IgnoreWhiteSpace='yes', 
                              RemoveWhiteSpace='yes', CreateElementMap='yes')
      self.xth.registerElementClass(Run)
      self.xth.registerElementClass(Context)
      self.xth.registerElementClass(Iteration)
      self.xth.registerElementClass(DataSet)
      try:
         self.saxp = kw['sax_parser']
      except:
         self.saxp = saxexts.make_parser()
      self.saxp.setDocumentHandler(self.xth)
      self.filename = filename
      self.run = None
      self.backup_on_change = kw.get('backups', 1)

   def __requires_run(self):
      if self.run == None:
         raise "you must either load() a file or start building a document"

   def getRun(self):
      self.__requires_run()
      return self.run

   def load(self):
      Ok=None
      try:
         self.saxp.parse(self.filename)
         document = self.xth.getDocument()
         self.run = document.getChild('Run')
      except IOError,e:
         print "could not load or read %s" % self.filename
      except saxlib.SAXException,e:
         print "SAX Parser error %s " % e

   def save(self):
      self.__requires_run()
      local_time = time.localtime(time.time())
      if self.backup_on_change:
         todays_date = time.strftime('%m-%d-%Y', local_time)
         todays_time = time.strftime('%H.%M.%S', local_time)
         backup_filename = self.filename + '_' + todays_date + '_' + todays_time
         os.system('/bin/cp %s %s' % (self.filename, backup_filename))
      runAsXML = self.run.toXML()
      fp = open(self.filename, 'w')
      fp.write(runAsXML)
      fp.close()

def test1(filename='.md/Run1.xml'):
   rf = RunFile(filename)
   rf.load()
   cl_context = rf.run.createContext('compute_loop')
   iter1 = cl_context.nextIteration()
   iter2 = cl_context.nextIteration()
   iter1.createDataSet('rho', 'compute', 'enzo')
   iter2.createDataSet('rho', 'compute', 'enzo')
   iter1.createDataSet('rho_jpeg', 'render', 'enzo')
   iter2.createDataSet('rho_jpeg', 'render', 'enzo')
   rf.save()
   
def test2(filename='.md/Run1.xml'):
   rf = RunFile(filename)
   rf.load()
   cl_context = rf.run.getContext('compute_loop')
   iter1 = cl_context.nextIteration()
   print "iteration (from metadata) = %s" % iter1.getAttributes().getFirst('count')
   iter1.createDataSet('rho', 'compute', 'enzo')
   iter1.createDataSet('rho_jpeg', 'render', 'enzo')
   rf.save()

if __name__ == '__main__':
   if len(sys.argv) < 2:
      print "usage: ExecutionFile test1 or test2"
      sys.exit(1)
   method = vars()[sys.argv[1]]
   method()
