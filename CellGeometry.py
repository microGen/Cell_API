from operator import add, sub

class Geometry:
    """Base geometry, single vertex"""

    def __init__(self, location):
        self.__location = location

    def getLocation(self):
        return self.__location

########################################################################################################################
########################################################################################################################


class CompGeom(Geometry):
    """Complex, compound geometry, objects with multiple vertices"""

    def __init__(self, verts, location):
        self.__vertices = verts
        super().__init__(location)

    def getVertices(self):
        return self.__vertices

    def getVertexLocations(self):
        return [i.getLocation() for i in self.__vertices]

########################################################################################################################
########################################################################################################################


class Vertex(Geometry):
    """Single vertex representation"""

    def __init__(self, vert0):
        super().__init__(vert0)
        self.__location = vert0

########################################################################################################################
########################################################################################################################


class Edge(CompGeom):
    """Edge representation, consists of 2 vertices"""

    def __init__(self, vert0, vert1):
        position = [divisor / 2 for divisor in list(map(add, vert1.getLocation(), vert0.getLocation()))]
        super().__init__([vert0, vert1], position)

########################################################################################################################
########################################################################################################################


class Face(CompGeom):
    """Quad face representation, consists of 4 vertices"""

    def __init__(self, vert0, vert1, vert2, vert3):
        position = [divisor/2 for divisor in list(map(add, vert2.getLocation(), vert0.getLocation()))]
        super().__init__([vert0, vert1, vert2, vert3], position)