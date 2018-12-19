import socket    

class DataSender():
    """
    Class that handles communication with server, on initialisation will attempt to connect to server
    """

    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__closed_socket = False

        self.__socket = socket.socket()
        self.__socket.settimeout(60)
        self.__socket.connect((self.__host, int(self.__port)))

    def notify(self, msg): 
        """
        Sends message to server and waits for response
        Input: 
            msg: message to send to server
        """

        if self.__closed_socket == False: 
            self.__socket.send(msg.encode())
            response = self.__socket.recv(1024)
            print("Messge received from server:", response.decode())

            if 'err' == response.decode():
                raise socket.error('Recieved unexpected data from server')
            
            return response.decode()

    def send_data(self, data): 
        """
        High-performance send of file data 
        Input: 
            data: file data
        """

        if self.__closed_socket == False: 
            self.__socket.sendfile(data, 0)

    def close(self): 
        if self.__closed_socket == False: 
            self.__socket.close()   
            self.__closed_socket = True