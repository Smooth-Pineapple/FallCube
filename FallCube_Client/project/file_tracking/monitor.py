import os
import time

from file_tracking.file_tracking import FileTracking
from file_tracking.monitor_handle import MonitorHandle
from watchdog.observers import Observer

class Monitor(FileTracking):
  def __init__(self, dir, callBack):
    super().__init__(dir, callBack)
    self.__observer = Observer()

  def run(self):
    try:
      self.__observer.schedule(MonitorHandle(self._relevant_path_stripper), self._dir, recursive = True)
      self.__observer.start()
      try:
        while True:
            time.sleep(10)
      except KeyboardInterrupt:
        self.__observer.stop()

      self.__observer.join()
    except OSError:
      print("An error occured trying to read the file.")