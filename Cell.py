from operator import itemgetter
from CellGeometry import Vertex, Edge, Face

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

        '''
        local coordinate system:
        Z
        |  Y
        | /
        ______X

        Cell geometry count always stars at origin, goes ccw and up.
        So: vertex0:    [0, 0, 0],     |vertex2:    [1, 1, 0],     |vertex6:    [1, 1, 1]
            edge0:      v0->v1,        |edge4:      v0->v4,        |edge8:      v4->v5
            face0:      v0, v1, v2, v3 |face1:      v0, v1, v4, v5 |face5:      v4, v5, v6, v7
        '''

        #list of coordinates for cell vertices
        c_list = [[self.__minmax_coordinates[0][0], self.__minmax_coordinates[1][0], self.__minmax_coordinates[2][0]], \
                  [self.__minmax_coordinates[0][1], self.__minmax_coordinates[1][0], self.__minmax_coordinates[2][0]], \
                  [self.__minmax_coordinates[0][1], self.__minmax_coordinates[1][1], self.__minmax_coordinates[2][0]], \
                  [self.__minmax_coordinates[0][0], self.__minmax_coordinates[1][1], self.__minmax_coordinates[2][0]], \
                  [self.__minmax_coordinates[0][0], self.__minmax_coordinates[1][0], self.__minmax_coordinates[2][1]], \
                  [self.__minmax_coordinates[0][1], self.__minmax_coordinates[1][0], self.__minmax_coordinates[2][1]], \
                  [self.__minmax_coordinates[0][1], self.__minmax_coordinates[1][1], self.__minmax_coordinates[2][1]], \
                  [self.__minmax_coordinates[0][0], self.__minmax_coordinates[1][1], self.__minmax_coordinates[2][1]]]

        #list of vertices
        self.__vertices = [Vertex(c_list[i], i) for i in range(8)]

        #list of edges
        self.__edges = []
        self.__edges.extend([Edge(self.__vertices[i], self.__vertices[(i+1) & 3], i) for i in range(4)])
        self.__edges.extend([Edge(self.__vertices[i], self.__vertices[i+4], i+4) for i in range(4)])
        self.__edges.extend([Edge(self.__vertices[i], self.__vertices[((i+1) | 4) & 7], i+4) for i in range(4, 8)])

        #list of faces
        self.__faces = []
        self.__faces.append(Face(self.__vertices[0], self.__vertices[1], self.__vertices[2], self.__vertices[3], 0))
        self.__faces.extend([Face(self.__vertices[i], \
                                  self.__vertices[(i+1) & 3], \
                                  self.__vertices[((i+5) | 4) & 7], \
                                  self.__vertices[i+4], i+1) for i in range(4)])
        self.__faces.append(Face(self.__vertices[4], self.__vertices[5], self.__vertices[6], self.__vertices[7], 5))

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


class CellFinal(Cell):
    """Cell Prototype, used to build up cell structure. Finalized cells are handled by class Cell"""

    def __init__(self, serial_number, core_properties, ext_properties):
        super().__init__(serial_number, core_properties, ext_properties)

########################################################################################################################


    def generateVectors(self):
        pass

########################################################################################################################

