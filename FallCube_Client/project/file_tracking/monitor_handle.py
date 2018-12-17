import os

from watchdog.events import FileSystemEventHandler

class MonitorHandle(FileSystemEventHandler):
    def __init__(self, callBack):
        self.__callBack = callBack

        # Due to multiple modified eventrs being fored for one action, track modified time of each file and ignore subsecond modifications
        self.__mod_times = {}
        
    def __debug_event(self, event):
        if event.is_directory == False:
            self.__callBack(event.event_type, os.path.dirname(event.src_path), os.path.basename(event.src_path))
        else:
            self.__callBack(event.event_type, event.src_path, '')

    def on_created(self, event): 
        file_stat = os.stat(event.src_path)
        mod_time = file_stat.st_mtime
        if event.src_path not in self.__mod_times or mod_time - self.__mod_times[event.src_path] > 0.5:
            self.__debug_event(event)

        self.__mod_times[event.src_path] = mod_time
        
    def on_deleted(self, event): 
        self.__debug_event(event)

    def on_modified(self, event):
        if event.is_directory == False:
            file_stat = os.stat(event.src_path)
            mod_time = file_stat.st_mtime
            if event.src_path not in self.__mod_times or mod_time - self.__mod_times[event.src_path] > 0.5:
                self.__debug_event(event)

            self.__mod_times[event.src_path] = mod_time    
            
    def on_moved(self, event):
        self.__callBack(event.event_type, os.path.dirname(event.src_path), os.path.basename(event.dest_path), os.path.basename(event.src_path))