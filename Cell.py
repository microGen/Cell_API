from operator import itemgetter

class CellPrototype:
    """Cell Prototype, used to build up cell structure. Finalized cells are handled by class 'CellFinal'"""

    def __init__(self, serial_number, location, size, property_list, FEA_Data_transfer):    #refactor all FEA to data
        self.__ID = serial_number
        self.__coordinates = location
        self.__dimensions = size
        self.__properties = property_list
        self.__minmax_coordinates = []
        self.__FEA_data = FEA_Data_transfer

        for i in range(3):
            min = self.__coordinates[i] - self.__dimensions[i]/2
            max = self.__coordinates[i] + self.__dimensions[i]/2
            self.__minmax_coordinates.append([min, max])

########################################################################################################################


    def storeFEAData(self, FEA_data_transfer):
        self.__FEA_data.append(FEA_data_transfer)
        self.__FEA_data = sorted(self.__FEA_data, key=itemgetter(0))

########################################################################################################################


    def getFEAData(self):
        return self.__FEA_data

########################################################################################################################


    def splitCell(self):
        pass

########################################################################################################################


    def getID(self):
        return self.__ID

########################################################################################################################


    def getCoordinates(self):
        return self.__coordinates

########################################################################################################################


    def getDimensions(self):
        return self.__dimensions

########################################################################################################################


    def getProperties(self):
        return self.__properties

########################################################################################################################


    def getMinMax(self):
        return self.__minmax_coordinates

########################################################################################################################


    def isFinal(self):
        return False

########################################################################################################################


    def getData(self):
        data_list = []
        data_list.append(self.getID())
        data_list.extend([self.getCoordinates(), self.getDimensions(), self.getProperties(), self.getMinMax(), self.getFEAData()])
        return data_list



########################################################################################################################
########################################################################################################################
########################################################################################################################


class CellFinal(CellPrototype):
    """Cell Prototype, used to build up cell structure. Finalized cells are handled by class Cell"""

    def __init__(self, serial_number, location, size, property_list, FEA_Data_transfer):
        super().__init__(serial_number, location, size, property_list, FEA_Data_transfer)

########################################################################################################################


    def generateVectors(self):
        pass

########################################################################################################################

