#!/usr/bin/env python2.2

import sys
import os
import os.path
import string
import re

from xparser import XElementParser
from xelement import XElement

class Counter(object):
   def __init__(self):
      self.__count = 0

   def get_count(self):
      self.__count = self.__count + 1
      return self.__count
   count = property(get_count)

class Job(object, XElement):
   job_counter = Counter()

   def initialize(self):
      self.attributes = self.getAttributes()
      self.last_set = {}
      self.waits_for = {}
      if self.getName() == 'job':
         self.job_table_id = Job.job_counter.count

   def compute_last_set(self):
      self.last_set = { self : None }
      return self.last_set.copy()

   def push_waits_for(self, wait_set):
      self.waits_for.update(wait_set)

   def gen_sql(self, **extra_job_info):
      if self.getName() != 'job':
         return

      query_template = """
      INSERT INTO JobPart
         (username, job_ticket_id, job_part_id, user_defined_name,
          nodes, type, main_class, main_method, code, waits_for)
      VALUES ('%(username)s', %(job_ticket_id)s, %(job_table_id)s, '%(name)s',
              %(nodes)s, '%(type)s', '%(mainclass)s', '%(mainmethod)s', '%(code)s',
              '%(waits_for_csv)s')
      """

      waits_for_ids = []
      for job in self.waits_for:
         waits_for_ids.append( int(job.job_table_id) )
 
      query_env = {
         'job_table_id' : self.job_table_id,
         'name' : self.name,
         'nodes' : self.nodes,
         'type' : self.type,
         'mainclass' : self.mainclass,
         'mainmethod' : self.mainmethod,
         'code' : self.code,
         'waits_for_csv': str(waits_for_ids)[1:-1]
      }

      query_env.update(extra_job_info)
      query = query_template  % query_env
      return query

   def debug_last_set(self):
      last_set_job_names = []
      for job in self.last_set:
         last_set_job_names.append( str(job.job_table_id) )
      print "setting last_set"
      self.attributes['last_set'] = str(last_set_job_names)
      for node in self.getChildren():
         if isinstance(node, Job):
            node.debug_last_set()

   def debug_waits_for(self):
      waits_for_job_names = []
      for job in self.waits_for:
         waits_for_job_names.append( str(job.job_table_id) )
      print "setting waits_for"
      self.attributes['waits_for'] = str(waits_for_job_names)
      for node in self.getChildren():
         if isinstance(node, Job):
            node.debug_waits_for()

   def get_name(self):
      return self.attributes.getFirst('name')

   def get_type(self):
      return self.attributes.getFirst('type')

   def get_nodes(self):
      return self.attributes.getFirst('nodes')

   def get_code(self):
      return self.attributes.getFirst('code')

   def get_mainclass(self):
      return self.attributes.getFirst('mainclass')

   def get_mainmethod(self):
      return self.attributes.getFirst('mainmethod')

   def get_job_table_id(self):
      return self.attributes.getFirst('job_table_id')

   def set_job_table_id(self, value):
      self.attributes['job_table_id'] = value

   name = property(get_name)
   type = property(get_type)
   nodes = property(get_nodes)
   code = property(get_code)
   mainclass = property(get_mainclass)
   mainmethod = property(get_mainmethod)
   job_table_id = property(get_job_table_id, set_job_table_id)

class JobSeq(Job):
   def initialize(self):
      Job.initialize(self)

   def push_waits_for(self, wait_set):
      self.waits_for.update(wait_set)
      last_set_pushed = wait_set
      for node in self.getChildren():
          node.push_waits_for(last_set_pushed)
          last_set_pushed = node.last_set

   def compute_last_set(self):
      for node in self.getChildren():
         last_set = node.compute_last_set()
      self.last_set = last_set
      return self.last_set.copy()

class JobPar(JobSeq):
   def initialize(self):
      Job.initialize(self)

   def compute_last_set(self):
      for node in self.getChildren():
          last_set = node.compute_last_set()
          self.last_set.update(last_set)
      return self.last_set.copy()

   def push_waits_for(self, wait_set):
      self.waits_for.update(wait_set)
      for node in self.getChildren():
          node.push_waits_for(wait_set)

class Property(object, XElement):
   def initialize(self):
      self.attributes = self.getAttributes()

   def get_name(self):
      return self.attributes.getFirst('name')

   def get_value(self):
      return self.attributes.getFirst('value')

   def compute_last_set(self):
      return {}

   name = property(get_name)

   value = property(get_value)

class Ticket(object,XElement):
   ticket_counter = Counter()

   def compute_last_set(self):
      for node in self.getChildren():
          node.compute_last_set()

   def push_waits_for(self, wait_set={}):
      for node in self.getChildren():
          node.push_waits_for(wait_set)

   def debug_last_set(self):
      for node in self.getChildren():
          node.debug_last_set()

   def debug_waits_for(self):
      for node in self.getChildren():
          node.debug_waits_for()

if len(sys.argv) < 2:
   print "usage: create_job.py job1.xml job2.xml ..."
   sys.exit(1)

my_classes = { 'job' : Job, 'seq' : JobSeq, 'par' : JobPar, 
               'property' : Property, 'ticket' : Ticket }

ticket_id = 0
for job_file in sys.argv[1:]:
  ticket_id = ticket_id + 1
  xparser = XElementParser(my_classes)
  doc = xparser.process(job_file)
  doc.compute_last_set()
  #doc.debug_last_set()
  doc.push_waits_for()
  #doc.debug_waits_for()
  print "Generating job table entries"
  allJobs = xparser.xth.getElementMap()['job']
  for job in allJobs:
     print job.gen_sql(username='gkt', job_ticket_id=ticket_id)
     print
  #print doc.toXML()
