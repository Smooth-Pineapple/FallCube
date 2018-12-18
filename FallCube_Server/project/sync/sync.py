from abc import ABC, abstractmethod 

class Sync(ABC): 
    def set_sync_action(self, mode, file_type, remote_file, new_name = None):
        response = ''
        if mode == 'created':
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

    @abstractmethod
    def set_file_sync(self, path):raise NotImplementedError   
    @abstractmethod   
    def sync_file_data(self, data):raise NotImplementedError
    @abstractmethod    
    def finished_file_sync(self):raise NotImplementedError   
    @abstractmethod
    def sync_dir(self, path):raise NotImplementedError

        