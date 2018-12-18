import os

from watchdog.events import FileSystemEventHandler

class MonitorHandle(FileSystemEventHandler):
    def __init__(self, callBack):
        self.__callBack = callBack

        # Due to multiple modified eventrs being fored for one action, track modified time of each file and ignore subsecond modifications
        self.__mod_times = {}
        
    def __handle_event(self, isDir, eType, path_dir, path_file, path_old_file = None):
        if eType == 'deleted':
            self.__callBack(eType, os.path.dirname(path_dir), os.path.basename(path_file), path_old_file)
            return

        file_stat = os.stat(path_file)
        mod_time = file_stat.st_mtime
        if path_file not in self.__mod_times or mod_time - self.__mod_times[path_file] > 0.5:
            #pof = None
            #if path_old_file is not None:
            #    pof = path_old_file

            if isDir == False:
                eType = eType + ',file'
            else:
                eType = eType + ',dir'

            self.__callBack(eType, os.path.dirname(path_dir), os.path.basename(path_file), path_old_file)

        self.__mod_times[path_file] = mod_time 

    def on_created(self, event): 
        self.__handle_event(event.is_directory, event.event_type, event.src_path, event.src_path)
        
    def on_deleted(self, event): 
        self.__handle_event(event.is_directory, event.event_type, event.src_path, event.src_path)

    def on_modified(self, event):
        if event.is_directory == False:
            self.__handle_event(event.is_directory, event.event_type, event.src_path, event.src_path)

    def on_moved(self, event):
        self.__handle_event(event.is_directory, event.event_type, event.dest_path, event.dest_path, event.src_path)