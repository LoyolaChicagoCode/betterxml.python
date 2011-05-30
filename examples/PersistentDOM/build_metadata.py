#!/usr/local/python-2.1/bin/python

import sys
import os
import os.path

from PXML import PElement

"""
We'll be encoding a test document:
<Execution name="enzo">
  <Run id="run-id">
     <Context name="...">
        <Iteration name="..." value="...">
           <DS name="ds-name" index="i" value="value of i"/>
           ...
        </Iteration>
     ...
   ...
...

This will be a series of programs to demonstrate the flexibility of the
persistent DOM.
"""

def create_application(dir_name, app_name):
   if os.path.exists(dir_name):
      print "%s exists; please specify a new directory." % dir_name

   e = PElement(dir_name)
   e.set_name('Execution')
   e.add_attribute('application_name', app_name)

def next_run(dir_name):
   e = PElement(dir_name)

   try:
      last_run = e.get_element(-1)
      next_run_id = int(last_run.get_first_attribute('id')) + 1
   except:
      next_run_id = 0

   e.add_element(1)
   this_run = e.get_element(-1)
   this_run.set_name('Run')
   this_run.add_attribute('id', next_run_id)

def get_run(dir_name, run_id):
   e = PElement(dir_name)
   run_count = e.get_element_count()
   run_element_id = None
   for i in range(0, run_count):
      run_element = e.get_element(i)
      if run_element.get_name() != 'Run':
         continue
      run_element_id = run_element.get_first_attribute('id')
      if str(run_element_id) == str(run_id):
         return run_element 
   return None

def get_context(dir_name, run_id, context_name):
   run_element = get_run(dir_name, run_id)
   context_count = run_element.get_element_count()
   for i in range(0, context_count):
      context_element = run_element.get_element(i)
      if context_element.get_name() != 'Context':
         continue
      context_element_name = context_element.get_first_attribute('name')
      if context_element_name == context_name:
         return context_element
   return None

def new_context(dir_name, run_id, context_name):
   run_element = get_run(dir_name, run_id)
   context_element = get_context(dir_name, run_id, context_name)
   if context_element == None:
      run_element.add_element(1)
      context_element = run_element.get_element(-1)
      context_element.set_name('Context')
      context_element.add_attribute('name', context_name)
   return context_element

def get_iteration(dir_name, run_id, context_name, index_name, index_value):
   context_element = get_context(dir_name, run_id, context_name)
   iter_count = run_element.get_element_count()
   for i in range(0, iter_count):
      iter_element = iter_element.get_element(i)
      if iter_element.get_name() != 'Iteration':
         continue
      iter_element_name = iter_element.get_first_attribute('index_name')
      iter_element_value = iter_element.get_first_attribute('index_value')
      if iter_element_name == index_name and iter_index_value == str(index_value):
         return iter_element
   return None

def add_iteration(dir_name, run_id, context_name, index_name, index_value):
   context_element = get_context(dir_name, run_id, context_name)
   if context_element.get_element_count():
      last_iter = context_element.get_element(-1)
      last_iter_index_name = last_iter.get_first_attribute('index_name')
      if last_iter_index_name != index_name:
         raise "attempt to change loop index from %s to %s" % (last_iter_index_name, index_name)
   context_element.add_element(1)
   this_iter = context_element.get_element(-1)
   this_iter.set_name('Iteration')
   this_iter.add_attribute('index_name', index_name)
   this_iter.add_attribute('index_value', index_value)
   return this_iter

def add_dataset(iter_element, phase_name, ds_name, ds_filename):
   if iter_element.get_name() != 'Iteration':
      raise "You must give me an 'Iteration' object."
   iter_element.add_element(1)
   ds_element = iter_element.get_element(-1)
   ds_element.set_name('DataSet')
   ds_element.add_attribute('phase_name', phase_name)
   ds_element.add_attribute('ds_name', ds_name)
   ds_element.add_attribute('ds_filename', ds_filename)
   return ds_element

def get_dataset(iter_element, phase_name, ds_name):
   for i in range(0, iter_element.get_element_count()):
       ds_element = iter_element.get_element(i)
       if ds_element.get_first_attribute('phase_name') == phase_name and ds_element.get_first_attribute('ds_name') == ds_name:
          return ds_element
   return None
   
def phase1():
   create_application('xyz', 'enzo')
   next_run('xyz')
   next_run('xyz')
   c1 = new_context('xyz', 0, 'computation_loop')
   c2 = new_context('xyz', 1, 'computation_loop')
   for i in range(0, 10):
      iter_handle = add_iteration('xyz', 0, 'computation_loop', 'i', i)
      add_dataset(iter_handle, 'compute', 'rho', 'rho%d' % i)
      add_dataset(iter_handle, 'compute', 'rho-debug', 'rho-debug%d' % i)

   for j in range(0, 10):
      iter_handle = add_iteration('xyz', 1, 'computation_loop', 'j', j)
      add_dataset(iter_handle, 'compute', 'v', 'v%d' % j)

   e = PElement('xyz')
   print e.toXML()

def phase2():
   c1 = get_context('xyz', 0, 'computation_loop')
   for i in range(0,c1.get_element_count()):
      this_iter = c1.get_element(i)
      ds = get_dataset(this_iter, 'compute', 'rho-debug')
      ds_name =  ds.get_first_attribute('ds_name')
      iter_count = this_iter.get_first_attribute('index_value')
      add_dataset(this_iter, 'render', 'rho_jpeg_file', 'rho%d.jpg' % iter_count)

   e = PElement('xyz')
   print e.toXML()

if __name__ == '__main__':
   phases = { 'phase1' : phase1, 'phase2' : phase2 }
   if len(sys.argv) < 2:
      print "usage: build_metadata.py phase1|phase2|..."
   else:
      phases[ sys.argv[1] ]()
