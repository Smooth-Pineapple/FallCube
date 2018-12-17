import sys
import socket

from file_transfer.data_receiver import DataReceiver

class FileTransfer():
    def __init__(self, dir, host, port):
        self.__data_receiver = DataReceiver(host, port)
        self.__base_dir = dir

    def run(self):
        if self.__data_receiver.is_closed() == False:
            try:
                self.__data_receiver.connect()
                while True:
                    client_socket = self.__data_receiver.accept()[0]

                    if client_socket is not None:
                        print('receiving data...')
                        data = client_socket.recv(1024)
                        print('data=%s mode', (data))
                        client_socket.send('ok'.encode())

                        data = client_socket.recv(1024)
                        print('data=%s', (data))  
                        while data:
                            data = client_socket.recv(1024)
                            print('data=%s', (data))   

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
