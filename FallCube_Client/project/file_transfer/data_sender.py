import socket    

class DataSender():
    def __init__(self, host, port):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host = host
        self.__port = port
        self.__closed_socket = False
          
    def connect(self, mode): 
        if self.__closed_socket == False: 
            self.__socket.connect((self.__host, int(self.__port)))
            self.send(mode)

    def send(self, data): 
        if self.__closed_socket == False: 
            self.__socket.send(data)

    def close(self): 
        if self.__closed_socket == False: 
            self.__socket.close()   
            self.__closed_socket = True

    def is_closed(self): 
        return self.__closed_socket