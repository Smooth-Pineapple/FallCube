import os 
import shutil

from sync.sync import Sync

class FileIOSync(Sync): 
    """
    Implementation of Sync class to handle client directory events via local file system actions
    """

    def __init__(self, dir):
        """
        Input:
            dir: local directory path to synchronise with client
        """

        self.__download_dir = dir
        self.__file = None

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
        # Can't modify/ delete/ move a non-existent file/ directory
        if not os.path.exists(self.__download_dir + remote_file) and (mode == 'modified' or  mode == 'deleted' or mode == 'move'):
            response = 'end'
        elif mode == 'created' and os.path.exists(self.__download_dir + remote_file):# Can't create a file/ directory that already exists
            response = 'end'
        else:
            response = super().set_sync_action(mode, file_type, remote_file, new_name)

        return response

    def set_file_sync(self, path):
        """
        Open file handler
        Input:
            path: path(relative to synchronised directory) to create file
        """

        if not self.__file:
            self.__file = open(self.__download_dir + path, 'wb+')

    def sync_file_data(self, data):
        """
        Write data to file
        Input:
            data: data to write
        """

        if self.__file:
            self.__file.write(data)

    def end_file_sync(self):
        """
        Close file handler
        """

        if self.__file:
            self.__file.close() 
            self.__file = None       

    def sync_dir(self, path):
        """
        Create directory
        Input:
            path: path(relative to synchronised directory) to create directory
        """

        os.makedirs(self.__download_dir + path)

    def sync_delete(self, path):
        """
        Delete file/ directory
        Input:
            path: path(relative to synchronised directory) to delete file/ directory
        """

        # Try to remove directory tree, if this fails remove as a file
        try:
            shutil.rmtree(self.__download_dir + path)
        except OSError:
            os.remove(self.__download_dir + path)

    def sync_rename(self, new, old):
        """
        Deal with renaming of file/ directory
        Input:
            new: path(relative to synchronised directory) of new file name
            old: path(relative to synchronised directory) of old file name
        """

        # Get path to new file
        new_path = self.__download_dir + os.path.dirname(new)
        # If this path contains non-existent directories make them
        if not os.path.isdir(new_path):
            os.makedirs(new_path)

        # If this new file name doesn't exist in the destination, move it there
        if not os.path.exists(self.__download_dir + new):
            shutil.move(self.__download_dir + old, self.__download_dir + new)
        else:
            # Clean up leftovers
            if os.path.exists(self.__download_dir + old):
                os.rmdir(self.__download_dir + old)

    def __del__(self):
        self.end_file_sync()
        