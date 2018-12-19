from abc import ABC, abstractmethod
 
import os

class FileTracking(ABC):
  """
  Abstract class to be used to track file system for files/ directories
  """

  def __init__(self, dir, call_back):
    self._dir = dir
    self.__call_back = call_back

  def _callback_with_relevant_path_stripper(self, action, path, file, old_path = None):
    """
    Invokes callback using path from monitored directory
    Input:
        action: type of file system event (created, modified, deleted, moved), and whether it applies to a file/ directory
        path: full path to file/ directory
        file: file/ directory that is relevant to event
        old_file: (optional) if renaming(moved) this will contain path to the old file/ directory(inc path)
    """

    # Remove full path to determine path of file relative to monitored directory
    relevant_path = path.replace(self._dir, '')
    if old_path:
      # Renaming
      old_relevant_path = old_path.replace(self._dir, '')
      self.__call_back(action, relevant_path, file, old_relevant_path)
    else:
      self.__call_back(action, relevant_path, file)

  @abstractmethod
  def run(self):
    raise NotImplementedError("Subclass must implement abstract method")