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
                        server_response = file_sync.set_sync_method(data.decode())

                        client_socket.send(server_response.encode())
 
                        while data:
                            data = client_socket.recv(1024)
                            print(data.decode()) 

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
