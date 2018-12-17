import os

class FileTracking:
  def __init__(self, dir, callBack):
    self._dir = dir
    self.__callBack = callBack

  def _relevant_path_stripper(self, action, path, file, old_name = None):
    relevant_path = path.replace(self._dir, '')
    if action == 'moved' and old_name:
      self.__callBack(action, relevant_path, [old_name, file])
    else:
      self.__callBack(action, relevant_path, file)

  def run(self):
    raise NotImplementedError("Subclass must implement abstract method")