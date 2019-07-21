import Factories
from FileIO import FileIO

debug_cell = False
debug_json = False

print('Hello World, this is the testing stage for the cell structure as of now')

loc = [1, 1, 1]
dim = [2, 2, 2]

c = Factories.cellFactory(3, loc, dim, {}, False)
cont = Factories.containerFactory("json_test_input.txt")

if debug_cell:
    print('Cell data:')
    print('ID:\t\t\t', c.ID())
    print('Pos:\t\t', c.location())
    print('Dims:\t\t', c.dimensions())
    print('MinMax:\t\t', c.minmax())
    print('Volume:\t\t', c.volume())
    print('CoreProps:\t', c.coreProperties())
    print('ExtProps:\t', c.extProperties())
    print(c.vertices(), '\n')
    print(c.vertices(1), '\n')
    print(c.vertices([0, 2, 3]), '\n')
    print(c.edges(), '\n')
    print(c.faces(), '\n')

if debug_json:
    print('Input Data:')
    print(cont.dumpData())
    print(cont.getNearestData([-432432, -42343242, 4234324]))
    print(cont.getEnclosedData([[4, 5], [4, 5], [4, 5]]))
    print(cont.getData([[4, 5], [4, 5], [4, 5]]))
    print('Data fields:\t\t', cont.lengthOfData())

fio = FileIO("json_test_input.txt", 'r')
print(fio.dumpData())
fio.closeFile()
fio.loadFile("testfile.txt", 'r')
print(fio.dumpData())