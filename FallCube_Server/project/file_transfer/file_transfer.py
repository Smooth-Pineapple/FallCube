import os
import sys
import socket

from file_transfer.data_receiver import DataReceiver
from file_sync.file_sync import FileSync

class FileTransfer():
    def __init__(self, dir, host, port):
        self.__data_receiver = DataReceiver(host, port)
        self.__base_dir = dir

    def run(self):
        if self.__data_receiver.is_closed() == False:
            try:
                self.__data_receiver.connect()
                file_sync = FileSync(self.__base_dir)

                while True:
                    client_socket = self.__data_receiver.accept()[0]

                    if client_socket is not None:
                        data = client_socket.recv(1024)

                        decoded_data = data.decode()
                        mode = decoded_data.split(',')[0]
                        file_type = decoded_data.split(',')[1]
                        remote_file = decoded_data.split(',')[-1]
                        new_name = ''
                        if mode == 'moved':
                           new_name = decoded_data.split(',')[-2]

                        server_response = file_sync.set_sync_method(mode, file_type, remote_file, new_name)

                        client_socket.send(server_response.encode())

                        if server_response == 'read':
                            file_sync.create_and_open_file(remote_file)
                            while data:
                                data = client_socket.recv(1024)
                                file_sync.write_to_file(data)
                                print(data.decode()) 
                            file_sync.close_file()   
                        elif server_response == 'create':
                            file_sync.create_dir(remote_file)
            except socket.error as e:
                print("Error in socket connection:", e)
                self.close()  
            except socket.gaierror as e:
                print("Error with address:", e)       
                self.close()  
            except:
                print("Unexpected error:", sys.exc_info()[0])    
                self.close()               
        else:
            print("Socket is closed")

    def close(self):
        self.__data_receiver.close()   
