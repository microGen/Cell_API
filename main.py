import Factories
from FileIO import FileIO
import Testing
import Rulebook
import ExtPropCalc
import Helpers
from Arbiter import Arbiter

debug_cell = False
debug_json = False
debug_rules = False

print('Testing stage for Cell API\n')

Testing.cell_unit_test()
Testing.container_unit_test()
Testing.prop_calc_unit_test()

loc = [1, 1, 1]
dim = [2, 2, 2]

### CHANGE DENSITY BACK TO MAT DENSITY WHEN CALCULATOR IS IMPLEMENTED ###
c = Factories.cellFactory(3, loc, dim, {'density': 0.00787, 'wall_thickness': 0.2}, False)
cont = Factories.containerFactory("json_test_input.txt")

print('\n\n--- EXPERIMENTAL AREA ---\n')

if debug_cell:
    print('Cell data:')
    print('ID:\t\t\t', c.ID())
    print('Pos:\t\t', c.properties('location'))
    print('Dims:\t\t', c.properties('dimensions'))
    print('Volume:\t\t', c.properties('volume'))
    print('CoreProps:\t', c.properties('location', 'dimensions', 'volume'))
    print('ExtProps:\t', c.properties('mat_density'))
    print(c.vertices(), '\n')
    print(c.vertices(1), '\n')
    print(c.vertices(0, 2, 3), '\n')
    print(c.edges(), '\n')
    print(c.faces(), '\n')

if debug_json:
    print('Input Data:\t\t\t', cont.dumpData())
    print('Nearest Data:\t\t', cont.getNearestGridPoints([-432432, -42343242, 4234324]))
    print('Enclosed Data:\t\t', cont.getEnclosedGridPoints([[4, 5], [4, 5], [4, 5]]))
    print('All Data:\t\t\t', cont.getGridPoints([[4, 5], [4, 5], [4, 5]]))
    print('Data fields:\t\t', cont.lengthOfData())

if debug_rules:
    print(c.properties('dimensions'))
    print('prop:', ExtPropCalc.CellDensity.getProp(), 'ressources: ', ExtPropCalc.CellDensity.getResources())
    dens = ExtPropCalc.CellDensity.calc(c.properties('dimensions'), 0.2, c.properties('mat_density'))
    print('Nearest Data:\t\t', cont.getNearestGridPoints([-432432, -42343242, 4234324]))
    print(dens)
    print(Rulebook.Density_min.getProp())
    print(Rulebook.Density_min.apply(cont.getNearestGridPoints([-432432, -42343242, 4234324]), dens))

#print(ExtPropCalc.CellDensity.getResources())
#print(Rulebook.Density_min.getResources())
#print(Rulebook.Density_min.apply(cont.getNearestGridPoints([-432432, -42343242, 4234324]), 0.0023))

a = Factories.arbiterFactory(cont)
print('Cell Density < Grid Density? ', a.applyRules(c, [Rulebook.Density_min], 1, ['min'], [ExtPropCalc.CellDensity]))