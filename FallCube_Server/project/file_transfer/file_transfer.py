import os
import sys
import socket

from file_transfer.data_receiver import DataReceiver
from sync.file_io_sync import FileIOSync

class FileTransfer():
    def __init__(self, dir, host, port):
        self.__data_receiver = DataReceiver(host, port)
        self.__base_dir = dir

    def run(self):
        if self.__data_receiver.is_closed() == False:
            try:
                self.__data_receiver.connect()
                sync = FileIOSync(self.__base_dir)

                while True:
                    client_socket = self.__data_receiver.accept()[0]

                    if client_socket is not None:
                        data = client_socket.recv(1024)
                        mode, file_type, remote_file, new_name = self.__parse_client_request(data)

                        server_response = sync.set_sync_action(mode, file_type, remote_file, new_name)
                        client_socket.send(server_response.encode())

                        if server_response == 'read':
                            sync.set_file_sync(remote_file)
                            while data:
                                data = client_socket.recv(1024)
                                sync.sync_file_data(data)
                                print(data.decode()) 
                            sync.finished_file_sync()   
                        elif server_response == 'create':
                            sync.sync_dir(remote_file)
            except IOError as e:
                print("IOError error:", e)                   
            except socket.error as e:
                print("Error in socket connection:", e)
            except socket.gaierror as e:
                print("Error with address:", e)       
            except:
                print("Unexpected error:", sys.exc_info()[0])    
            finally:
                self.close()               
        else:
            print("Socket is closed")

    def __parse_client_request(self, data):
        decoded_data = data.decode()

        mode = decoded_data.split(',')[0]
        file_type = decoded_data.split(',')[1]
        remote_file = decoded_data.split(',')[-1]
        new_name = ''

        if mode == 'moved':
            new_name = decoded_data.split(',')[-2]

        return mode, file_type, remote_file, new_name

    def close(self):
        self.__data_receiver.close()   
