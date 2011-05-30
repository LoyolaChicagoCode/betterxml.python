import sys
import os
import os.path

import BootstrapMetadata
from ExecutionFile import ExecutionFile
from RunFile import RunFile

class FileSet:
   def __init__(self, fileset, current_phase="undefined"):
      if os.path.exists(fileset):
         if not os.path.isdir(fileset):
            raise "fileset %s is not a directory" % fileset
      else:
         os.mkdir(fileset)

      self.fileset_fullpath = os.path.abspath(fileset)
      self.current_phase = current_phase
      self.__check_metadata()
      self.__check_data()
      self.__load_execution_file()

   def __check_metadata(self):
      """
      Internal method to check whether the metadata directory exists. If
      it does, it had better not be corrupted. If this is the first time
      being run, we bootstrap the Executions.xml file.
      """
      self.executions_file = None
      metadata_dir = os.path.join(self.fileset_fullpath, '.md')
      if os.path.exists(metadata_dir):
         if not os.path.isdir(metadata_dir):
            raise "corrupted metadata directory %s" % metadata_dir
      else:
         os.mkdir(metadata_dir)

      self.metadata_dir = metadata_dir
      self.executions_file = os.path.join(metadata_dir, 'Executions.xml')
      print "writing execution file %s" % self.executions_file
      if not os.path.exists(self.executions_file):
         fp = open(self.executions_file, 'w')
         fp.write(BootstrapMetadata.EXECUTIONS_FILE)
         fp.close()
      else:
         pass # meaning, it is ok--Executions.xml exists from a previous init

   def __check_data(self):
      """
      Internal method to check whether the data directory exists. If
      it does, it had better be a directory. Otherwise, it is considered
      corrupt. If this is the first time, we create it for the user.
      """
      data_dir = os.path.join(self.fileset_fullpath, '.d')
      if os.path.exists(data_dir):
         if not os.path.isdir(data_dir):
            raise "corrupted data directory %s" % metadata_dir
      else:
         os.mkdir(data_dir)

   def __load_execution_file(self):
      self.execution_md = ExecutionFile(self.executions_file)
      self.execution_md.load()
      self.execution = self.execution_md.getExecution()

   def next_run(self):
      self.current_run = self.execution_md.execution.nextRun(self.metadata_dir)
      self.current_run_id = self.current_run.getAttributes().getFirst('id')
      self.__load_run_file()

   def latest_run(self):
      current_run_id = self.execution_md.execution.getMaxRun()
      self.current_run = self.execution_md.execution.getRun(current_run_id)
      self.current_run_id = current_run_id
      self.__load_run_file()

   def previous_run(self):
      self.latest_run()
      current_id = self.current_run.getAttributes().getFirst('id')
      current_id = int(current_id)
      if current_id > 0:
         current_id = current_id - 1
      self.current_run = self.execution_md.execution.getRun(current_id)
      self.current_run_id = current_id
      self.__load_run_file()

   def __load_run_file(self):
      run_id = self.current_run.getAttributes().getFirst('id')
      run_file_name = 'Run%s.xml' % run_id
      run_file_path = os.path.join(self.metadata_dir, run_file_name)
      self.run_file_md = RunFile(run_file_path)
      self.run_file_md.load()
      self.current_run = self.run_file_md.getRun()
      print "type of current run %s" % self.current_run.__class__.__name__

   def __requires_run(self):
      if not hasattr(self,'current_run'):
         raise "need to call next_run(), latest_run(), or current_run()"

   def get_context(self, context_name):
      self.__requires_run()
      self.current_context = self.current_run.getContext(context_name)

   def new_context(self, context_name):
      self.__requires_run()
      self.current_run.createContext(context_name)
      self.current_context = self.current_run.getContext(context_name)

   # XYZ: Go back and add the user_index, user_iteration information
   def __requires_context(self):
      if not hasattr(self, 'current_context'):
         raise "need to call get_context() or new_context()"

   def next_iter(self):
      self.__requires_context()
      self.current_iteration = self.current_context.nextIteration()

   # XYZ: Not done yet.
   def record_event(self, description, props):
      self.__requires_context()

   def __requires_iteration(self):
      if not hasattr(self, 'current_iteration'):
         raise "no current iteration"

   def get_dataset(self, dataset_name):
      self.__requires_iteration()
      self.current_iteration.getDataSet(dataset_name, self.current_phase)

   def new_dataset(self, dataset_name):
      fileset_name  = self.current_iteration.createDataSet(dataset_name, self.current_phase, self.current_run_id)
      return os.path.join(self.fileset_fullpath, fileset_name)

   def commit(self):
      self.__requires_run()
      self.run_file_md.save()
      self.execution_md.save()

   def __str__(self):
      return str(dir(self))

