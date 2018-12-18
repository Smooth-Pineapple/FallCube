import os

from file_tracking.file_tracking import FileTracking

class ScanOnce(FileTracking):
  def run(self):
    try:
      for path, dirName, fileName in os.walk(self._dir):
          if fileName != [] or dirName != []:
            for file in fileName:         
              self._relevant_path_stripper('created|file', path, file)
            for dir in dirName:         
              self._relevant_path_stripper('created|dir', path, dir)

    except OSError as e:
      print("An error occured trying to read the file:", e)