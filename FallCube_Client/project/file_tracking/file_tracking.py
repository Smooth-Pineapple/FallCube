from abc import ABC, abstractmethod
 
import os

class FileTracking(ABC):
  def __init__(self, dir, callBack):
    self._dir = dir
    self.__callBack = callBack

  def _relevant_path_stripper(self, action, path, file, old_path = None):
    relevant_path = path.replace(self._dir, '')
    if old_path:
      old_relevant_path = old_path.replace(self._dir, '')
      self.__callBack(action, relevant_path, file, old_relevant_path)
    else:
      self.__callBack(action, relevant_path, file)

  @abstractmethod
  def run(self):
    raise NotImplementedError("Subclass must implement abstract method")