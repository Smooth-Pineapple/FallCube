import os
import sys
import socket

from file_transfer.data_receiver import DataReceiver
from sync.file_io_sync import FileIOSync

class FileTransfer():
    """
    Class that deals with file/ directory event information from client
    """

    def __init__(self, dir, host, port):
        """
        Input: 
            dir: path of synchronised directory
            host: host to run on
            port: port to run on
        """

        self.__data_receiver = DataReceiver(host, port)
        self.__base_dir = dir

    def run(self):
        """
        Listens for messages from client and invokes synchronisation actions
        """

        try:
            # Connect to socket
            self.__data_receiver.connect()
            # Synchronisation method
            sync = FileIOSync(self.__base_dir)

            while True:
                # Accept communications from client
                client_socket = self.__data_receiver.accept()[0]

                if client_socket is not None:
                    # Wait for message detailing client directory event
                    data = client_socket.recv(1024)

                    mode, file_type, remote_file, new_name = self.__parse_client_request(data)

                    # Understand how server will react to event and tell client
                    server_response = sync.set_sync_action(mode, file_type, remote_file, new_name)
                    client_socket.send(server_response.encode())

                    if server_response == 'read':
                        # A file has been created/ modified so write to local directory
                        sync.set_file_sync(remote_file)
                        while data:
                            data = client_socket.recv(1024)
                            sync.sync_file_data(data)
                            
                        sync.end_file_sync()   
                    elif server_response == 'create':
                        # A directory has been created
                        sync.sync_dir(remote_file)

                    elif server_response == 'remove':
                        # A file/ directory has been deleted
                        sync.sync_delete(remote_file)

                    elif server_response == 'rename':
                        # A file/ directory has been renamed
                        sync.sync_rename(new_name, remote_file)

        except OSError as e:
            print("OSError error:", e)                   
        except socket.error as e:
            print("Error in socket connection:", e)
        except socket.gaierror as e:
            print("Error with address:", e)       
        except:
            print("Unexpected error:", sys.exc_info()[0])    
        finally:
            self.close()               

    def __parse_client_request(self, data):
        """
        Output:
            mode: event type(created, modified, deleted, moved)
            file_type: file or directory(file, dir)
            remote_file: file/ directory relevant to event
            new_name: file/ directory name after renaming (empty if not renamed)
        """

        decoded_data = data.decode()
        print("Server recieved message:", decoded_data) 

        mode = decoded_data.split('|')[0]
        file_type = decoded_data.split('|')[1]
        remote_file = decoded_data.split('|')[-1]
        new_name = ''

        if mode == 'moved':
            new_name = decoded_data.split('|')[-2]

        return mode, file_type, remote_file, new_name

    def close(self):
        self.__data_receiver.close()   
