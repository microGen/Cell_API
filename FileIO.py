class FileIO:
    'Basic class to handle File input/output'

    def __init__(self, filename, mode):
        self._input_file = filename
        try:
            self.io_file = open(self._input_file, mode)
        except:
            print('File name or mode invalid.')

    def changeFile(self, filename, mode):
        try:
            self.io_file.close();
            self.io_file = open(filename, mode)
        except:
            print('File name or mode invalid.')
