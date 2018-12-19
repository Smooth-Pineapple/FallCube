import os

from file_tracking.file_tracking import FileTracking

class ScanOnce(FileTracking):
  """
  Implementation of FileTracking class to do a initial scan of directory for files/ directories
  """

  def run(self):
    """
    Scans directory for files/ directories, then calls method to to get relative path of file/ directory and invoke call back method
    """

    try:
      for path, dirName, fileName in os.walk(self._dir):
          if fileName != [] or dirName != []:
            for file in fileName:         
              self._callback_with_relevant_path_stripper('created|file', path, file)
            for dir in dirName:         
              self._callback_with_relevant_path_stripper('created|dir', path, dir)

    except OSError as e:
      print("An error occured trying to read the file:", e)