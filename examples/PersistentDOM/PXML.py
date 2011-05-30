#
# I believe we need to focus on "elements" in the quest for the perfect
# disk-based DOM. Thus I will start here.
#

"""
design note:

name file contains the namespace and element name as a tuple and pickled.

attrs file contains a list of k/v pairings in a list of tuples, pickled.

elements are self-similar, just in subdirs. More on that in a bit.
"""

import os
import os.path
import cPickle as pickle
import tempfile

class PElement:
   PE_NAME_FILE = '_N_'
   PE_ATTRS_FILE = '_A_'
   PE_ELEMENTS_FILE = '_E_'
   PE_TEXT_FILE = '_T_'       # only appears in text elements.
   def __init__(self, dir, **kw):
      is_text = kw.get('type','element') == 'text'
      self.dir = os.path.abspath(dir)
      self.pe_name_file = os.path.join(self.dir, PElement.PE_NAME_FILE)
      self.pe_attrs_file = os.path.join(self.dir, PElement.PE_ATTRS_FILE)
      self.pe_elements_file = os.path.join(self.dir, PElement.PE_ELEMENTS_FILE)
      self.pe_text_file = os.path.join(self.dir, PElement.PE_TEXT_FILE)
      self.__check_dir_exists()
      self.__check_dir_structure()
      if is_text:
         self.__add_text_file()
         self.set_name(':T')

   def __check_dir_exists(self):
      if not os.path.exists(self.dir):
         os.mkdir(self.dir)

   def __check_dir_structure(self):
      if not os.path.exists(self.pe_name_file):
         fp = open( self.pe_name_file, 'w')
         p = pickle.Pickler(fp)
         p.dump((None, None))
         fp.close()
      if not os.path.exists(self.pe_attrs_file):
         fp = open(self.pe_attrs_file, 'w')
         p = pickle.Pickler(fp)
         p.dump([])
         fp.close()
      if not os.path.exists(self.pe_elements_file):
         fp = open(self.pe_elements_file, 'w')
         p = pickle.Pickler(fp)
         p.dump({})
         fp.close()

   def __add_text_file(self):
      if not os.path.exists(self.pe_text_file):
         fp = open( self.pe_text_file, 'w')
         p = pickle.Pickler(fp)
         p.dump((None, None))
         fp.close()

   def get_namespace(self):
      fp = open(self.pe_name_file, 'r')
      u = pickle.Unpickler(fp)
      (ns, name) = u.load()
      fp.close()
      return ns

   def get_name(self):
      fp = open(self.pe_name_file, 'r')
      u = pickle.Unpickler(fp)
      (ns, name) = u.load()
      return name

   def get_fq_name(self):
      fp = open(self.pe_name_file, 'r')
      u = pickle.Unpickler(fp)
      return u.load()

   def set_name(self, name, ns=None):
      fp = open(self.pe_name_file, 'w')
      p = pickle.Pickler(fp)
      p.dump( (ns, name) )
      fp.close()

   def get_attributes(self, in_set=[]):
      fp = open(self.pe_attrs_file, 'r')
      u = pickle.Unpickler(fp)
      attr_list = u.load()
      fp.close()
      if not in_set:
         return attr_list
      else:
         select_list = []
         for pair in attr_list:
            if pair[0] in in_set:
               select_list.append(pair)
         return select_list

   def get_first_attribute(self, name):
      all_pairs = self.get_attributes([name])
      if not all_pairs:
         return None
      else:
         return all_pairs[0][1]


   def add_attribute(self, name, value):
      attr_list = self.get_attributes()
      attr_list.append( (name, value) )
      fp = open(self.pe_attrs_file, 'w')
      p = pickle.Pickler(fp)
      p.dump(attr_list)
      fp.close()

   def change_attribute(self, name, value):
      attr_list = self.get_attributes()
      for i in range(0, len(attr_list)):
         (attr_name, attr_value) =  attr_list[i]
         if attr_name == name:
            attr_list[i] = (name, value)
            break
      fp = open(self.pe_attrs_file, 'w')
      p = pickle.Pickler(fp)
      p.dump(attr_list)
      fp.close()

   def set_text(self, text):
      if not self.is_text():
         raise "not a text node"
      fp = open(self.pe_text_file, 'w')
      fp.write(text)
      fp.close()

   def get_text(self):
      if self.is_text():
         fp = open(self.pe_text_file, 'r')
         text = fp.read()
         fp.close()
         return text
      raise "not a text node"


   def add_element(self, how_many=1, text_only=0):
      fp = open(self.pe_elements_file, 'r')
      u = pickle.Unpickler(fp)
      element_map = u.load()
      tempfile.tempdir = self.dir
      if not element_map.keys():
         new_element_id = 0
      else:
         all_ids = element_map.keys()
         all_ids.sort()
         new_element_id = all_ids[-1] + 1

      for i in range(0, how_many):
         element_id = new_element_id + i
         element_dir_name = tempfile.mktemp()
         element_dir_fp = os.path.join(self.dir, element_dir_name)
         os.mkdir(element_dir_fp)
         if text_only:
            pe = PElement(element_dir_fp, type='text')
         else:
            pe = PElement(element_dir_fp, type='element')
         element_map[element_id] = element_dir_name

      fp = open(self.pe_elements_file, 'w')
      p = pickle.Pickler(fp)
      p.dump(element_map)
      fp.close()


   def add_cdata_element(self, how_many=1):
      self.add_element(how_many, 1)

   def is_text(self):
      return os.path.exists(self.pe_text_file)

   def get_element(self, i):
      fp = open(self.pe_elements_file, 'r')
      u = pickle.Unpickler(fp)
      element_map = u.load()
      if i < 0:
         i = i + len(element_map.keys())
      element_dir_name = element_map[i]
      element_dir_fp = os.path.join(self.dir, element_dir_name)
      return PElement(element_dir_fp)

   def get_element_count(self):
      fp = open(self.pe_elements_file, 'r')
      u = pickle.Unpickler(fp)
      element_map = u.load()
      return len(element_map.keys())


   def __str__(self):
      return self.toXML()

   def __indent(self, level):
      return '  ' * level

   def toXML(self, level=0):
      if self.is_text():
         return self.__indent(level+1) + self.get_text() + '\n'

      s = ''
      fq_name = self.get_fq_name()
      if fq_name[0] == None:
         name = fq_name[1]
      else:
         name = '%s:%s' % fq_name
      s = s + self.__indent(level) + ('<%s' % name)
      for attr_pair in self.get_attributes():
         s = s + (' %s="%s"' % attr_pair)
      s = s + '>' + '\n'
      for i in range(0, self.get_element_count()):
         s = s + self.get_element(i).toXML(level + 1)

      s = s + self.__indent(level) + ('</%s>' % name) + '\n'
      return s


