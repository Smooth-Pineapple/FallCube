import socket    

class DataReceiver():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__closed_socket = False
        
        self.__socket = socket.socket()
        
    def connect(self): 
        if self.__closed_socket == False: 
            self.__socket.bind((self.__host, int(self.__port)))
            self.__socket.listen(5)

    def accept(self): 
        if self.__closed_socket == False: 
            return self.__socket.accept()
        return None    

    def close(self): 
        if self.__closed_socket == False: 
            self.__socket.close()   
            self.__closed_socket = True