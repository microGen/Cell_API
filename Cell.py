from operator import itemgetter
from CellGeometry import Vertex, Edge, Face
from ExtPropCalc import MinMaxCoordinates

class Cell:
    """Cell Prototype, used to build up cell structure. Finalized cells are handled by class 'CellFinal'"""

    def __init__(self, serial_number, location, dimensions, ext_properties):
        self.__properties = {'location': location, 'dimensions': dimensions}
        self.__properties.update(ext_properties)

        self.__ID = serial_number
        self.__final = False

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

        self.__minmax = MinMaxCoordinates.calc([self.__properties['location'], self.__properties['dimensions']])

        #list of coordinates for cell vertices
        c_list = [[self.__minmax[0][0], self.__minmax[1][0], self.__minmax[2][0]], \
                  [self.__minmax[0][1], self.__minmax[1][0], self.__minmax[2][0]], \
                  [self.__minmax[0][1], self.__minmax[1][1], self.__minmax[2][0]], \
                  [self.__minmax[0][0], self.__minmax[1][1], self.__minmax[2][0]], \
                  [self.__minmax[0][0], self.__minmax[1][0], self.__minmax[2][1]], \
                  [self.__minmax[0][1], self.__minmax[1][0], self.__minmax[2][1]], \
                  [self.__minmax[0][1], self.__minmax[1][1], self.__minmax[2][1]], \
                  [self.__minmax[0][0], self.__minmax[1][1], self.__minmax[2][1]]]

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

        self.__properties.update({'volume': \
            self.__edges[0].getLength() * self.__edges[1].getLength() * self.__edges[4].getLength()})

    ####################################################################################################################


    def splitCell(self):
        pass

    ####################################################################################################################


    def ID(self):
        return self.__ID

    ####################################################################################################################

    def vertices(self, *vertexID):
        if vertexID == ():
            return self.__vertices
        else:
            vertexID = vertexID[0]
            if type(vertexID) == int:
                return self.__vertices[vertexID]
            else:
                ret_vertices = []
                for i in vertexID:
                    ret_vertices.append(self.__vertices[i])
                return ret_vertices

    ####################################################################################################################


    def edges(self, *edgeID):
        if edgeID == ():
            return self.__edges
        else:
            edgeID = edgeID[0]
            if type(edgeID) == int:
                return self.__edges[edgeID]
            else:
                ret_edges = []
                for i in edgeID:
                    ret_edges.append(self.__edges[i])
                return ret_edges

    ####################################################################################################################


    def faces(self, *faceID):
        if faceID == ():
            return self.__faces
        else:
            faceID = faceID[0]
            if type(faceID) == int:
                return self.__faces[faceID]
            else:
                ret_faces = []
                for i in faceID:
                    ret_faces.append(self.__faces[i])
                return ret_faces


    ####################################################################################################################


    def properties(self, *key):
        if not key:
            return self.__properties
        else:
            if len(key) > 1:
                props = []
                for i in key:
                    props.append(self.__properties[i])
                return props
            else:
                return self.__properties[key[0]]

    ####################################################################################################################

    def setFinal(self):
        if not self.__final:
            self.__final = True

    ####################################################################################################################


    def isFinal(self):
        return self.__final




########################################################################################################################
########################################################################################################################


class CellFinal(Cell):
    """Cell Prototype, used to build up cell structure. Finalized cells are handled by class Cell"""

    def __init__(self, serial_number, location, dimensions, ext_properties):
        super().__init__(serial_number, location, dimensions, ext_properties)

    ####################################################################################################################


    def generateVectors(self):
        pass

########################################################################################################################

