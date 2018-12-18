import os 

from sync.sync import Sync

class FileIOSync(Sync): 
    def __init__(self, dir):
        self.__download_dir = dir
        self.__file = None

    def set_sync_action(self, mode, file_type, remote_file, new_name = None):
        print(mode, file_type, remote_file, new_name)

        response = ''
        if not os.path.exists(self.__download_dir + remote_file) and (mode == 'modified' or  mode == 'deleted' or mode == 'move'):
            response = 'end'
        elif mode == 'created' and os.path.exists(self.__download_dir + remote_file):
            response = 'end'
        else:
            response = super().set_sync_action(mode, file_type, remote_file, new_name)

        return response

    def set_file_sync(self, path):
        if not self.__file:
            self.__file = open(self.__download_dir + path, 'wb+')

    def sync_file_data(self, data):
        if self.__file:
            self.__file.write(data)

    def finished_file_sync(self):
        if self.__file:
            self.__file.close() 
            self.__file = None       

    def sync_dir(self, path):
        os.makedirs(self.__download_dir + path)

    def __del__(self):
        self.finished_file_sync()
        