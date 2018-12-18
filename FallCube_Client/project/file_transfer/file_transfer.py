import os 
import sys
import socket

from file_transfer.data_sender import DataSender

class FileTransfer():
    def __init__(self, dir, host, port):
        self.__host = host
        self.__port = port
        self.__base_dir = dir

    def transfer(self, event, dir, file, old_file = None):
        data_sender = DataSender(self.__host, self.__port)
    
        if data_sender.is_closed() == False:
            try:
                to_file = dir + os.sep + file
                if old_file:
                    to_file += ',' + old_file

                print(event + "," + to_file)
                
                server_response = data_sender.notify((event + ',' + to_file))
                if server_response == 'read':
                    file_to_parse = open(self.__base_dir + to_file, 'rb')
                    data_sender.send_data(file_to_parse)
                    file_to_parse.close()
                #else:
                #    data_sender.send_msg(file.encode())

            except FileNotFoundError as e:
                print("File not found:", e)   
            except socket.timeout as e:
                print("Socket timeout:", e) 
            except socket.error as e:
                print("Error in socket connection:", e)    
            except socket.gaierror as e:
                print("Error with address:", e)         
            except:
                print("Unexpected error:", sys.exc_info()[0])         
            finally:  
                data_sender.close()           
        else:
            print("Socket is closed")

        
