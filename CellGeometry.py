"""Cell Framework
Copyright (c) 2019 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)

Simple geometry implementation to represent rectangular hexahedrons"""

from operator import add
from math import sqrt

class Geometry:
    """Base geometry, single vertex"""

    def __init__(self, location, geometry_ID):
        self.__location = location
        self.__geometry_ID = geometry_ID

    def get_location(self):
        """Returns location of geometry object"""
        return self.__location

    def get_ID(self):
        """Returns ID of geometry object"""
        return self.__geometry_ID


class CompGeom(Geometry):
    """Complex, compound geometry, objects with multiple vertices"""

    def __init__(self, verts, location, geometry_ID):
        self.__vertices = verts
        super().__init__(location, geometry_ID)

    def get_vertices(self):
        """Returns list of vertices comprising geometry object"""
        return self.__vertices

    def get_vertex_locations(self):
        """Returns list of vertex locations from vertices comprising geometry object"""
        return [i.get_location() for i in self.__vertices]


class Vertex(Geometry):
    """Single vertex representation"""

    def __init__(self, coords, geometry_ID):
        self.__position = coords
        super().__init__(self.__position, geometry_ID)


class Edge(CompGeom):
    """Edge representation, consists of 2 vertices"""

    def __init__(self, vert0, vert1, geometry_ID):
        self.__vert0 = vert0
        self.__vert1 = vert1
        position = [divisor / 2 for divisor in list(map(add, vert1.get_location(), vert0.get_location()))]
        super().__init__([self.__vert0, self.__vert1], position, geometry_ID)

    def get_length(self):
        """Returns length of edge geometry object"""
        v0_loc = self.__vert0.get_location()
        v1_loc = self.__vert1.get_location()
        return sqrt((v0_loc[0] - v1_loc[0])**2 + (v0_loc[1] - v1_loc[1])**2 + (v0_loc[2] - v1_loc[2])**2)


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
        position = [divisor / 2 for divisor in list(map(add, vert2.get_location(), vert0.get_location()))]
        super().__init__([self.__vert0, self.__vert1, self.__vert2, self.__vert3], position, geometry_ID)

    def get_edge_lengths(self):
        """Returns length of edges comprising face geometry object as list"""
        return [self.__edge0.get_length(), self.__edge1.get_length()]#

    def get_area(self):
        """Returns area of face geometry object"""
        return self.__edge0.get_length() * self.__edge1.get_length()
