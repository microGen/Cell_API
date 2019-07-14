from Cell import Cell, CellFinal
from CellGeometry import *
from Arbiter import Arbiter
from FileIO import FileIO

print('Hello World, this is the testing stage for the cell structure as of now')

loc = [1, 1, 1]
dim = [2, 2, 2]

c = Cell(3, loc, dim, {})
print('Cell data:')
print('ID:\t\t\t', c.getID())
print('Pos:\t\t', c.getCoordinates())
print('Dims:\t\t', c.getDimensions())
print('MinMax:\t\t', c.getMinMax())
print('Volume:\t\t', c.getVolume())
print('CoreProps:\t', c.getCoreProperties())
print('ExtProps:\t', c.getExtProperties())

print(c.getVertices(), '\n')
print(c.getVertices(1), '\n')
print(c.getVertices([0,2,3]), '\n')
print(c.getEdges(), '\n')
print(c.getFaces(), '\n')