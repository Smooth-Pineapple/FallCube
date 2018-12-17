import sys
import socket

from file_reader.file_reader import FileReader
from file_transfer.data_sender import DataSender

class FileTransfer():
    def __init__(self, dir, host, port):
        self.__data_sender = DataSender(host, port)
        self.__base_dir = dir

    def transfer(self, event, dir, file):
        #created, deleted, modified, move
        print(event, dir, file)
    
        if self.__data_sender.is_closed() == False:
            try:
                self.__data_sender.connect(event)
                if file != '':
                    file_to_parse = FileReader.from_valid_path(self.__base_dir + dir + '/' + file, 1024)
                    if file_to_parse != None:
                        r = file_to_parse.init_read()
                        while r:
                            self.__data_sender.send(r)
                            r = file_to_parse.read()
                        file_to_parse.close()
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
        self.__data_sender.close()   
