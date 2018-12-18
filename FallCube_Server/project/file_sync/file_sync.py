import os 

class FileSync: 
    def __init__(self, dir):
        self.__download_dir = dir
        self.__local_files = set()

    def set_sync_method(self, data):
        print(data)

        mode = data.split(',')[0]
        remote_file = data.split(',')[-1]
        exists = remote_file in self.__local_files

        response = ''

        if mode == 'created' and exists:
            response = 'no'
        elif mode == 'modified' or mode == 'created':
            self.__local_files.add(remote_file)
            response = 'ok'
        elif mode == 'deleted' and exists:
            self.__local_files.add(remote_file)
            response = 'ok'
        elif mode == 'move' and not exists:
            response = 'no'
        elif  mode == 'move' and exists:
            self.__local_files.add(remote_file)
            response = 'ok'
        else:
            response = 'no'

        return response