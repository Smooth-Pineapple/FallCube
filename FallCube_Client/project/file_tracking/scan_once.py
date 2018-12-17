import os

from file_tracking.file_tracking import FileTracking

class ScanOnce(FileTracking):
  def run(self):
    try:
      for path, _, fileName in os.walk(self._dir):
          if fileName != []:
            for file in fileName:         
              self._relevant_path_stripper('created', path, file)
          else:
            self._relevant_path_stripper('created', path, '')

    except IOError:
      print("An error occured trying to read the file.")