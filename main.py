from Cell import Cell, CellFinal
from CellGeometry import Edge, Face
from Arbiter import Arbiter
from FileIO import FileIO

print('Hello World')

loc = [1, 2, 3]
dim = [4, 5, 6]

c = Cell(3, loc, dim, {})
e = Edge([1,0,1], [3,3,3])
f = Face([1, 1, 1], [2, 1, 1.5], [2, 2, 2], [1, 2, 1.5])

print(e.getLocation())
print(f.getLocation())