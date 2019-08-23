from operator import itemgetter
from CellGeometry import Vertex, Edge, Face
from Helpers import MinMaxCoordinates


class Cell:
    """Cell Prototype, used to build up cell structure. Finalized cells are handled by class 'CellFinal'"""

    def __init__(self, serial_number, location, dimensions, ext_properties):
        self._properties = {'location': location, 'dimensions': dimensions}
        self._properties.update(ext_properties)

        self._ID = serial_number
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

        self._minmax = MinMaxCoordinates.calc(self._properties['location'], self._properties['dimensions'])

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

        self._properties.update({'volume': \
                                     self._edges[0].get_length() * self._edges[1].get_length() * self._edges[4].get_length()})
        self._properties.update({'vertices': self.vertices, 'edges': self.edges, 'faces': self.faces})

    def split(self):
        """Returns cell properties, so that these can be transferred to sub-cells"""
        pass

    def ID(self):
        """Returns the ID of the cell"""
        return self._ID

    def vertices(self, *vertexID):
        """Returns list of cell vertices if no argument is given, else returns vertices of given IDs."""
        if vertexID == ():
            return self._vertices
        else:
            vertexID = vertexID[0]
            if type(vertexID) == int:
                return self._vertices[vertexID]
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
            edgeID = edgeID[0]
            if type(edgeID) == int:
                return self._edges[edgeID]
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
            faceID = faceID[0]
            if type(faceID) == int:
                return self._faces[faceID]
            else:
                ret_faces = []
                for i in faceID:
                    ret_faces.append(self._faces[i])
                return ret_faces

    def properties(self, *key):
        """Returns all properties if no argument is given, else returns property with given keys"""
        if not key:
            return self._properties
        else:
            if len(key) > 1:
                props = []
                for i in key:
                    props.append(self._properties[i])
                return props
            else:
                return self._properties[key[0]]

    def set_final(self):
        """Sets state of cell to final"""
        if not self._final:
            self._final = True

    def is_final(self):
        """Returns state of cell: True if final, false if still splittable."""
        return self._final


class CellFinal(Cell):
    """Cell Prototype, used to build up cell structure. Finalized cells are handled by class Cell"""

    def __init__(self, serial_number, location, dimensions, ext_properties):
        super().__init__(serial_number, location, dimensions, ext_properties)

    def generate_paths(self):
        pass
