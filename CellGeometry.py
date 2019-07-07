from operator import add, sub

class Geometry:
    def __init__(self, location):
        self.__location = location

    def getLocation(self):
        return self.__location


class Vertex(Geometry):
    def __init__(self, vert0):
        super().__init__()
        self.__location = vert0


class Edge(Geometry):
    def __init__(self, vert0, vert1):
        position = [divisor/2 for divisor in list(map(add, vert1, vert0))]
        super().__init__(position)


class Face(Geometry):
    def __init__(self, vert0, vert1, vert2, vert3):
        position = [divisor/2 for divisor in list(map(add, vert2, vert0))]
        super().__init__(position)