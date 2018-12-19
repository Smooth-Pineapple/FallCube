from abc import ABC, abstractmethod 

class Sync(ABC): 
    """
    Abstract class to synchronise with client files/ directories
    """

    def set_sync_action(self, mode, file_type, remote_file, new_name = None):
        """
        Understand client event
        Input:
            mode: type of file system event (created, modified, deleted, moved)
            file_type: whether event applies to a file/ directory
            remote_file: path(relative to monitored directory) to file/ directory that is relevant to event
            new_name: (optional) if renaming, this will contain path(relative to monitored directory) to the new file/ directory
        """

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
    def end_file_sync(self):raise NotImplementedError   
    @abstractmethod
    def sync_dir(self, path):raise NotImplementedError
    @abstractmethod
    def sync_delete(self, path):raise NotImplementedError
    @abstractmethod
    def sync_rename(self, path):raise NotImplementedError

        