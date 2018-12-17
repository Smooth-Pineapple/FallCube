import os 
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
                self.__data_sender.notify(event)
                if file != '':
                    file_to_parse = open(self.__base_dir + dir + '/' + file, 'rb')
                    self.__data_sender.send_data(file_to_parse)
                    file_to_parse.close()
                else:
                    self.__data_sender.send_msg(dir)

            except FileNotFoundError as e:
                print("File not found:", e)
                self.__data_sender.close()   
            except socket.timeout as e:
                print("Socket timeout:", e)
                self.__data_sender.close()   
            except socket.error as e:
                print("Error in socket connection:", e)
                self.__data_sender.close()    
            except socket.gaierror as e:
                print("Error with address:", e)       
                self.__data_sender.close()    
            except:
                print("Unexpected error:", sys.exc_info()[0])    
                self.__data_sender.close()                
        else:
            print("Socket is closed")

        
