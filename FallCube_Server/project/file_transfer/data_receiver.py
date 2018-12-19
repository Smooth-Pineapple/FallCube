import socket    

class DataReceiver():
    """
    Class that handles communication with client
    """

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__closed_socket = False
        
        self.__socket = socket.socket()
        
    def connect(self): 
        """
        Bind to host and port, allowing a max of 5 requests
        """

        if self.__closed_socket == False: 
            self.__socket.bind((self.__host, int(self.__port)))
            self.__socket.listen(5)

    def accept(self): 
        """
        Start accepting connections
        """

        if self.__closed_socket == False: 
            return self.__socket.accept()
        return None    

    def close(self): 
        if self.__closed_socket == False: 
            self.__socket.close()   
            self.__closed_socket = True