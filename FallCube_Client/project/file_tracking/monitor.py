import os
import time

from file_tracking.file_tracking import FileTracking
from file_tracking.monitor_handle import MonitorHandle
from watchdog.observers import Observer

class Monitor(FileTracking):
  """
  Implementation of FileTracking class to do a monitor directory for file/ directory changes
  """

  def __init__(self, dir, callBack):
    super().__init__(dir, callBack)
    self.__observer = Observer()

  def run(self):
    """
    Monitors directory for changes to files/ directories
    """

    try:
      # Monitor directory using MonitorHandle to handle file system changes
      self.__observer.schedule(MonitorHandle(self._callback_with_relevant_path_stripper), self._dir, recursive = True)
      self.__observer.start()
      try:
        while True:
            time.sleep(10)
      except KeyboardInterrupt:
        self.__observer.stop()

      self.__observer.join()
    except OSError:
      print("An error occured trying to read the file.")