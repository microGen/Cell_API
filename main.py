from Cell import Cell, CellFinal
from CellGeometry import *
from Arbiter import Arbiter
from FileIO import FileIO

print('Hello World')

loc = [1, 2, 3]
dim = [4, 5, 6]

c = Cell(3, loc, dim, {})


v1 = Vertex([1, 1, 1])
v2 = Vertex([2, 2, 2])
v3 = Vertex([3, 3, 3])
v4 = Vertex([4, 4, 4])
e = Edge(v1, v2)
f = Face(v1, v2, v3, v4)


print(e.getLocation())
print(e.getVertices())
print(e.getVertexLocations())