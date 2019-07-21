class FileIO:
    'Basic class to handle File input/output'

    def __init__(self, *args):
        self.__io_file = None
        if args != ():
            self.__io_file = open(args[0], args[1])


    ####################################################################################################################

    def __del__(self):
        if self.__io_file:
            self.__io_file.close()


    ####################################################################################################################

    def loadFile(self, *args):
        if self.__io_file:
            self.__io_file.close()
        self.__io_file = open(args[0], args[1])


    ####################################################################################################################

    def closeFile(self):
        if self.__io_file:
            self.__io_file.close()


    ####################################################################################################################

    def dumpData(self):
        return self.__io_file.read()