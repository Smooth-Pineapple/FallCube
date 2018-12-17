import os 

class FileReader: 
    def __init__(self, path, size): 
        self.__path = path 
        self.__size = size 
        self.__file = None
      
    @classmethod
    def from_valid_path(cls, path, size): 
        if os.path.isfile(path):
            return cls(path, size)
        else:
            return None

    def init_read(self):
        self.__file = open(self.__path, 'rb')

        return self.__file.read(self.__size)

    def read(self):
        if self.__file != None:
            return self.__file.read(self.__size)
        else:
            return None
        
    def close(self):
        if self.__file != None:
            self.__file.close