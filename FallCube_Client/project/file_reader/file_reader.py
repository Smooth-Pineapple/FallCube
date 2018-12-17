import os 

class FileReader: 
    def __init__(self, path): 
        self.__path = path 
        self.__file = None
      
    @classmethod
    def from_valid_path(cls, path): 
        if os.path.isfile(path):
            return cls(path)
        else:
            return None

    def open(self):
        self.__file = open(self.__path, 'rb')

        return self.__file

    def close(self):
        if self.__file != None:
            self.__file.close