import Factories
from FileIO import FileIO
import Testing

debug_cell = False
debug_json = True

print('Hello World, this is the testing stage for the cell structure as of now')

Testing.cell_unit_test()
Testing.container_unit_test()
Testing.prop_calc_unit_test()

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
    print('Input Data:\t\t\t', cont.dumpData())
    print('Nearest Data:\t\t', cont.getNearestData([-432432, -42343242, 4234324]))
    print('Enclosed Data:\t\t', cont.getEnclosedData([[4, 5], [4, 5], [4, 5]]))
    print('All Data:\t\t\t', cont.getData([[4, 5], [4, 5], [4, 5]]))
    print('Data fields:\t\t', cont.lengthOfData())

