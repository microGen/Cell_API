from operator import add, sub

class Geometry:
    """Base geometry, single vertex"""

    def __init__(self, location, geoID):
        self.__location = location
        self.__geoID = geoID

    def getLocation(self):
        return self.__location

    def getID(self):
        return self.__geoID

########################################################################################################################
########################################################################################################################


class CompGeom(Geometry):
    """Complex, compound geometry, objects with multiple vertices"""

    def __init__(self, verts, location, geoID):
        self.__vertices = verts
        super().__init__(location, geoID)

    def getVertices(self):
        return self.__vertices

    def getVertexLocations(self):
        return [i.getLocation() for i in self.__vertices]

########################################################################################################################
########################################################################################################################


class Vertex(Geometry):
    """Single vertex representation"""

    def __init__(self, coords, geoID):
        self.__position = coords
        super().__init__(self.__position, geoID)

########################################################################################################################
########################################################################################################################


class Edge(CompGeom):
    """Edge representation, consists of 2 vertices"""

    def __init__(self, vert0, vert1, geoID):
        position = [divisor / 2 for divisor in list(map(add, vert1.getLocation(), vert0.getLocation()))]
        super().__init__([vert0, vert1], position, geoID)

########################################################################################################################
########################################################################################################################


class Face(CompGeom):
    """Quad face representation, consists of 4 vertices"""

    def __init__(self, vert0, vert1, vert2, vert3, geoID):
        position = [divisor/2 for divisor in list(map(add, vert2.getLocation(), vert0.getLocation()))]
        super().__init__([vert0, vert1, vert2, vert3], position, geoID)