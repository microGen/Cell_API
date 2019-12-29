"""Cell Framework
Copyright (c) 2019 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)

Cell class, building block for infill structure"""

#from operator import itemgetter
from CellGeometry import Vertex, Edge, Face
from Helpers import MinMaxCoordinates


class Cell:
    """Cell class, used to build up cell structure"""

    def __init__(self, serial_number, location, dimensions, ext_properties):
        self._ID = serial_number
        self._geometry = {'location': location, 'dimensions': dimensions}
        self._ext_properties = ext_properties
        self._final = False

        # local coordinate system:
        # Z
        # |  Y
        # | /
        # ______X
        #
        # Cell geometry count always stars at origin, goes ccw and up.
        # So: vertex0:    [0, 0, 0],     |vertex2:    [1, 1, 0],     |vertex6:    [1, 1, 1]
        #     edge0:      v0->v1,        |edge4:      v0->v4,        |edge8:      v4->v5
        #     face0:      v0, v1, v2, v3 |face1:      v0, v1, v4, v5 |face5:      v4, v5, v6, v7

        self._minmax = MinMaxCoordinates.calc(self._geometry['location'], self._geometry['dimensions'])

        #list of coordinates for cell vertices
        c_list = [[self._minmax[0][0], self._minmax[1][0], self._minmax[2][0]], \
                  [self._minmax[0][1], self._minmax[1][0], self._minmax[2][0]], \
                  [self._minmax[0][1], self._minmax[1][1], self._minmax[2][0]], \
                  [self._minmax[0][0], self._minmax[1][1], self._minmax[2][0]], \
                  [self._minmax[0][0], self._minmax[1][0], self._minmax[2][1]], \
                  [self._minmax[0][1], self._minmax[1][0], self._minmax[2][1]], \
                  [self._minmax[0][1], self._minmax[1][1], self._minmax[2][1]], \
                  [self._minmax[0][0], self._minmax[1][1], self._minmax[2][1]]]

        #list of vertices
        self._vertices = [Vertex(c_list[i], i) for i in range(8)]

        #list of edges
        self._edges = []
        self._edges.extend([Edge(self._vertices[i], self._vertices[(i + 1) & 3], i) for i in range(4)])
        self._edges.extend([Edge(self._vertices[i], self._vertices[i + 4], i + 4) for i in range(4)])
        self._edges.extend([Edge(self._vertices[i], self._vertices[((i + 1) | 4) & 7], i + 4) for i in range(4, 8)])

        #list of faces
        self._faces = []
        self._faces.append(Face(self._vertices[0], self._vertices[1], self._vertices[2], self._vertices[3], 0))
        self._faces.extend([Face(self._vertices[i], \
                                 self._vertices[(i + 1) & 3], \
                                 self._vertices[((i + 5) | 4) & 7], \
                                 self._vertices[i + 4], i + 1) for i in range(4)])
        self._faces.append(Face(self._vertices[4], self._vertices[5], self._vertices[6], self._vertices[7], 5))

        self._geometry.update({'volume': \
                                     self._edges[0].get_length() * self._edges[1].get_length() * self._edges[4].get_length()})
        self._geometry.update({'vertices': self.vertices, 'edges': self.edges, 'faces': self.faces})

    def ID(self):
        """Returns the ID of the cell"""
        return self._ID

    def vertices(self, *vertexID):
        """Returns list of cell vertices if no argument is given, else returns vertices of given IDs."""
        if vertexID == ():
            return self._vertices
        else:
            if len(vertexID) == 1:
                return self._vertices[vertexID[0]]
            else:
                ret_vertices = []
                for i in vertexID:
                    ret_vertices.append(self._vertices[i])
                return ret_vertices

    def edges(self, *edgeID):
        """Returns list of cell edges if no argument is given, else returns edges of given IDs."""

        if edgeID == ():
            return self._edges
        else:
            if len(edgeID) == 1:
                return self._edges[edgeID[0]]
            else:
                ret_edges = []
                for i in edgeID:
                    ret_edges.append(self._edges[i])
                return ret_edges

    def faces(self, *faceID):
        """Returns list of cell faces if no argument is given, else returns faces of given IDs."""

        if faceID == ():
            return self._faces
        else:
            if len(faceID) == 1:
                return self._faces[faceID[0]]
            else:
                ret_faces = []
                for i in faceID:
                    ret_faces.append(self._faces[i])
                return ret_faces

    def properties(self, *key):
        """Returns all properties if no argument is given, else returns property with given keys"""

        properties = {**self._geometry, **self._ext_properties}

        if not key:
            return properties
        else:
            if len(key) > 1:
                props = []
                for k in key:
                    props.append(properties[k])
                return props
            else:
                return properties[key[0]]

    def geometry(self, *key):
        """Returns all cell geometry features if no argument is given, else returns following geometry featueres:
        - location [x, y, z]
        - dimensions [x, y, z]
        - volume
        - vertex getter method
        - edge getter method
        - face getter method"""

        if not key:
            return self._geometry
        else:
            if len(key) > 1:
                geo = []
                for k in key:
                    geo.append(self._geometry[k])
                return geo
            else:
                return self._geometry[key[0]]

    def ext_properties(self, *key):
        """Returns all externally given properties if no argument is given, else returns property with given keys"""

        if not key:
            return self._ext_properties
        else:
            if len(key) > 1:
                props = []
                for k in key:
                    props.append(self._ext_properties[k])
                return props
            else:
                return self._ext_properties[key[0]]

    def set_final(self):
        """Sets state of cell to final"""

        if not self._final:
            self._final = True

    def is_final(self):
        """Returns state of cell: True if final, false if still splittable."""
        return self._final

    def add_ext_property(self, keys, props):
        """Adds properties to cell's ext_prop dictionary.
        keys: key or list of keys
        props: property or list of properties. Must be of the same length as key_list"""

        if type(keys) == list:
            num_items = len(keys)
            for i in range(num_items):
                self._ext_properties.update({keys[i]: props[i]})
        else:
            self._ext_properties.update({keys: props})

    def add_ext_property(self, props):
        """Adds properties to cell's ext_prop dictionary.
        props: property or list of properties. Properties have to be key-value pairs, e.g. as calculated by External
            Property Calculators"""

        if type(props) == list:
            for prop in props:
                self._ext_properties.update(prop)
        else:
            self._ext_properties.update(props)

