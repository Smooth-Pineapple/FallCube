import socket    

class DataSender():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__closed_socket = False

        self.__socket = socket.socket()
        self.__socket.settimeout(90)
        self.__socket.connect((self.__host, int(self.__port)))

    def notify(self, mode): 
        if self.__closed_socket == False: 
            self.__socket.send(mode.encode())
            response = self.__socket.recv(1024)
            print(response.decode())

            if 'err' == response.decode():
                raise socket.error('Recieved unexpected data from server')
            
            return response.decode()

    def send_data(self, data): 
        if self.__closed_socket == False: 
            self.__socket.sendfile(data, 0)

    def close(self): 
        if self.__closed_socket == False: 
            self.__socket.close()   
            self.__closed_socket = True