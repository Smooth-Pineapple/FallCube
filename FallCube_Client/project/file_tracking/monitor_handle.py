import os

from watchdog.events import FileSystemEventHandler

class MonitorHandle(FileSystemEventHandler):
    """
    Class to handle file system events
    """

    def __init__(self, callBack):
        self.__callBack = callBack
        self.__mod_times = {}
        
    def _handle_event(self, isDir, eType, path_file, path_old_file = None):
        """
        Handle file system events
        Input:
            isDir: boolean representing input file/ directory
            eType: type of file system event (created, modified, deleted, moved)
            path_file: path to file/ directory (including name)
            path_old_file: (optional) path to file/ directory (before renaming)
        """

        # If file is deleted cant check for modified time so send through to call back 
        if eType == 'deleted':
            self.__callBack(eType, os.path.dirname(path_file), os.path.basename(path_file), path_old_file)
            return

        # Due to multiple modified events being fired for one action, track modified time of each file and ignore subsecond modifications
        file_stat = os.stat(path_file)
        mod_time = file_stat.st_mtime
        if path_file not in self.__mod_times or mod_time - self.__mod_times[path_file] > 0.5:
            if isDir == False:
                eType = eType + '|file'
            else:
                eType = eType + '|dir'

            self.__callBack(eType, os.path.dirname(path_file), os.path.basename(path_file), path_old_file)

        self.__mod_times[path_file] = mod_time 

    def on_created(self, event): 
        self._handle_event(event.is_directory, event.event_type, event.src_path)
        
    def on_deleted(self, event): 
        self._handle_event(event.is_directory, event.event_type, event.src_path)

    def on_modified(self, event):
        if event.is_directory == False:
            self._handle_event(event.is_directory, event.event_type, event.src_path)

    def on_moved(self, event):
        self._handle_event(event.is_directory, event.event_type, event.dest_path, event.src_path)