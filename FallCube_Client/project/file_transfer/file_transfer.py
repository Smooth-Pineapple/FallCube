import os 
import sys
import socket

from file_transfer.data_sender import DataSender

class FileTransfer():
    """
    Class that transfers files/ directories to server
    """

    def __init__(self, dir, host, port):
        """
        Input: 
            dir: path of monitored directory
            host: server host
            port: server port
        """

        self.__host = host
        self.__port = port
        self.__base_dir = dir

    def transfer(self, event, dir, file, old_file = None):
        """
        Attempts to transfer files/ directories to server 
        Input: 
            event: type of file system event (created, modified, deleted, moved), and whether it applies to a file/ directory
            dir: path to directory containing affected file/ directory  
            file: file/ directory that is relevant to event
            old_file: (optional) if renaming(moved) this will contain path to the old file/ directory(inc path)
        """

        # Object to handle server communication
        data_sender = DataSender(self.__host, self.__port)

        try:
            # Full path to affected file/ directory
            to_file = dir + os.sep + file
            if old_file:
                # Append previous path to affected file/ directory(renaming)
                to_file += '|' + old_file

            # Message to send to server, format:
                # [EVENT]|[FILE/DIRECTORY]|[PATH FROM MONITORED DIRECTORY TO FILE/ DIRECTORY]...also can have...|[PATH FROM MONITORED DIRECTORY TO OLD FILE/ DIRECTORY]
            client_msg = event + "|" + to_file
            print("Message to send to server:", client_msg)
            
            # Send message and wait for response
            server_response = data_sender.notify(client_msg)
            # If server is expecting to read file data, open local file and send data to server
            if server_response == 'read':
                file_to_parse = open(self.__base_dir + to_file, 'rb') 
                data_sender.send_data(file_to_parse)
                file_to_parse.close()

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
            data_sender.close() # Explicitly close even though destructor will do it anyway           

        
