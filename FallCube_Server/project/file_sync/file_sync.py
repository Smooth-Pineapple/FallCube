import os 

class FileSync: 
    def __init__(self, dir):
        self.__download_dir = dir
        self.__file = None

    def set_sync_method(self, mode, file_type, remote_file, new_name = None):
        print(mode, file_type, remote_file, new_name)

        response = ''
        if not os.path.exists(self.__download_dir + remote_file) and (mode == 'modified' or  mode == 'deleted' or mode == 'move'):
            response = 'end'
        elif mode == 'created' and os.path.exists(self.__download_dir + remote_file):
            response = 'end'
        elif mode == 'created':
            if file_type == 'file':
                response = 'read'
            else:
                response = 'create'    
        elif mode == 'modified':
            response = 'read'
        elif mode == 'moved':
            response = 'rename'    
        elif mode == 'deleted':
            response = 'remove'
        else:
            response = 'err'

        return response


    def create_and_open_file(self, path):
        if not self.__file:
            self.__file = open(self.__download_dir + path, 'wb+')

    def write_to_file(self, data):
        if self.__file:
            self.__file.write(data)

    def close_file(self):
        if self.__file:
            self.__file.close()        

    def create_dir(self, path):
        os.makedirs(self.__download_dir + path)

    def __del__(self):
        self.close_file()
        