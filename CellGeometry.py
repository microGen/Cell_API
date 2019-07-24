from operator import add
from math import sqrt

class Geometry:
    """Base geometry, single vertex"""

    def __init__(self, location, geometry_ID):
        self.__location = location
        self.__geometry_ID = geometry_ID

    ####################################################################################################################


    def getLocation(self):
        return self.__location

    ####################################################################################################################


    def getID(self):
        return self.__geometry_ID

########################################################################################################################
########################################################################################################################


class CompGeom(Geometry):
    """Complex, compound geometry, objects with multiple vertices"""

    def __init__(self, verts, location, geometry_ID):
        self.__vertices = verts
        super().__init__(location, geometry_ID)

    ####################################################################################################################


    def getVertices(self):
        return self.__vertices

    ####################################################################################################################


    def getVertexLocations(self):
        return [i.getLocation() for i in self.__vertices]

########################################################################################################################
########################################################################################################################


class Vertex(Geometry):
    """Single vertex representation"""

    def __init__(self, coords, geometry_ID):
        self.__position = coords
        super().__init__(self.__position, geometry_ID)

########################################################################################################################
########################################################################################################################


class Edge(CompGeom):
    """Edge representation, consists of 2 vertices"""

    def __init__(self, vert0, vert1, geometry_ID):
        self.__vert0 = vert0
        self.__vert1 = vert1
        position = [divisor / 2 for divisor in list(map(add, vert1.getLocation(), vert0.getLocation()))]
        super().__init__([self.__vert0, self.__vert1], position, geometry_ID)


    ####################################################################################################################

    def getLength(self):
        v0_loc = self.__vert0.getLocation()
        v1_loc = self.__vert1.getLocation()
        return sqrt((v0_loc[0] - v1_loc[0])**2 + (v0_loc[1] - v1_loc[1])**2 + (v0_loc[2] - v1_loc[2])**2)

########################################################################################################################
########################################################################################################################


class Face(CompGeom):
    """Quad face representation, consists of 4 vertices. Edges are calculated internally"""

    def __init__(self, vert0, vert1, vert2, vert3, geometry_ID):
        self.__vert0 = vert0
        self.__vert1 = vert1
        self.__vert2 = vert2
        self.__vert3 = vert3
        self.__edge0 = Edge(self.__vert0, self.__vert1, 0)
        self.__edge1 = Edge(self.__vert1, self.__vert2, 1)
        self.__edge2 = Edge(self.__vert2, self.__vert3, 2)
        self.__edge3 = Edge(self.__vert3, self.__vert0, 3)
        position = [divisor/2 for divisor in list(map(add, vert2.getLocation(), vert0.getLocation()))]
        super().__init__([self.__vert0, self.__vert1, self.__vert2, self.__vert3], position, geometry_ID)

    ####################################################################################################################


    def getEdgeLengths(self):
        return [self.__edge0.getLength(), self.__edge1.getLength()]#

    ####################################################################################################################


    def getArea(self):
        return self.__edge0.getLength() * self.__edge1.getLength()
