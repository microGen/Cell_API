from operator import itemgetter
from CellGeometry import *

class Cell:
    """Cell Prototype, used to build up cell structure. Finalized cells are handled by class 'CellFinal'"""

    def __init__(self, serial_number, location, size, ext_properties):
        self.__ID = serial_number
        self.__coordinates = location
        self.__dimensions = size
        self.__minmax_coordinates = []
        self.__ext_properties = ext_properties

        for i in range(3):
            min = self.__coordinates[i] - self.__dimensions[i] / 2
            max = self.__coordinates[i] + self.__dimensions[i] / 2
            self.__minmax_coordinates.append([min, max])


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
        return self.__core_properties['pos']

########################################################################################################################


    def getDimensions(self):
        return self.__core_properties['dim']

########################################################################################################################


    def getCoreProperties(self):
        return self.__core_properties

########################################################################################################################


    def getMinMax(self):
        return self.__minmax_coordinates

########################################################################################################################


    def isFinal(self):
        return False




########################################################################################################################
########################################################################################################################
########################################################################################################################


class CellFinal(Cell):
    """Cell Prototype, used to build up cell structure. Finalized cells are handled by class Cell"""

    def __init__(self, serial_number, core_properties, ext_properties):
        super().__init__(serial_number, core_properties, ext_properties)

########################################################################################################################


    def generateVectors(self):
        pass

########################################################################################################################

