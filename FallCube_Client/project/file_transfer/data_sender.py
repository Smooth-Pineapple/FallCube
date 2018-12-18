import socket    

class DataSender():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__closed_socket = False

        self.__socket = socket.socket()
        self.__socket.settimeout(30)
        self.__socket.connect((self.__host, int(self.__port)))

    def notify(self, mode): 
        if self.__closed_socket == False: 
            self.send_msg(mode.encode())
            response = self.__socket.recv(1024)
            print(response.decode())

            if 'ok' != response.decode() and 'no' != response.decode():
                raise socket.error('Recieved unexpected data from server')
            
            return response.decode()

    def send_msg(self, msg): 
        if self.__closed_socket == False: 
            self.__socket.send(msg)

    def send_data(self, data): 
        if self.__closed_socket == False: 
            self.__socket.sendfile(data, 0)

    def close(self): 
        if self.__closed_socket == False: 
            self.__socket.close()   
            self.__closed_socket = True

    def is_closed(self): 
        return self.__closed_socket