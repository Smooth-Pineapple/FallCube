import os

from watchdog.events import FileSystemEventHandler

class MonitorHandle(FileSystemEventHandler):
    def __init__(self, callBack):
        self.__callBack = callBack

        # Due to multiple modified eventrs being fored for one action, track modified time of each file and ignore subsecond modifications
        self.__mod_times = {}
        
    def __handle_event(self, isDir, eType, path_dir, path_file, path_old_file = None):
        pof = None
        if path_old_file is not None:
            pof = os.path.basename(path_old_file)

        if isDir == False:
            self.__callBack(eType, os.path.dirname(path_dir), os.path.basename(path_file), pof)
        else:
            self.__callBack(eType, path_dir, '', pof)

    def on_created(self, event): 
        file_stat = os.stat(event.src_path)
        mod_time = file_stat.st_mtime
        if event.src_path not in self.__mod_times or mod_time - self.__mod_times[event.src_path] > 0.5:
            self.__handle_event(event.is_directory, event.event_type, event.src_path, event.src_path)

        self.__mod_times[event.src_path] = mod_time
        
    def on_deleted(self, event): 
        self.__handle_event(event.is_directory, event.event_type, event.src_path, event.src_path)

    def on_modified(self, event):
        if event.is_directory == False:
            file_stat = os.stat(event.src_path)
            mod_time = file_stat.st_mtime
            if event.src_path not in self.__mod_times or mod_time - self.__mod_times[event.src_path] > 0.5:
                self.__handle_event(event.is_directory, event.event_type, event.src_path, event.src_path)

            self.__mod_times[event.src_path] = mod_time    
            
    def on_moved(self, event):
        self.__handle_event(event.is_directory, event.event_type, event.src_path, event.dest_path, event.src_path)