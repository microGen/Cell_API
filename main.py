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

c = Factories.CELL(3, loc, dim, {'mat_density': 0.00787, 'wall_thickness': 0.2}, False)
cont = Factories.CONTAINER("json_test_input.txt")
cont2 = Factories.CONTAINER("grid_data.json")

# cells = []
# id = 0
# for x in range(0, 11, 2):
#     for y in range(0, 11, 2):
#         for z in range(0, 11, 2):
#             cells.append(Factories.CELL(id, [x, y, z], dim, {'mat_density': 0.00787, 'wall_thickness': 0.2}, False))
#             id += 1

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
    print('Input Data:\t\t\t', cont.dump_data())
    print('Nearest Data:\t\t', cont.get_nearest_grid_points([-432432, -42343242, 4234324]))
    print('Enclosed Data:\t\t', cont.get_enclosed_grid_points([[4, 5], [4, 5], [4, 5]]))
    print('All Data:\t\t\t', cont.get_grid_points([[4, 5], [4, 5], [4, 5]]))
    print('Data fields:\t\t', cont.length_of_data())

if debug_rules:
    print(c.properties('dimensions'))
    print('prop:', ExtPropCalc.CellDensity.get_prop(), 'ressources: ', ExtPropCalc.CellDensity.get_resources())
    dens = ExtPropCalc.CellDensity.calc(c.properties('dimensions'), 0.2, c.properties('mat_density'))
    print('Nearest Data:\t\t', cont.get_nearest_grid_points([-432432, -42343242, 4234324]))
    print(dens)
    print(Rulebook.Density_min.get_prop())
    print(Rulebook.Density_min.apply(cont.get_nearest_grid_points([-432432, -42343242, 4234324]), dens))

#print(ExtPropCalc.CellDensity.get_resources())
#print(Rulebook.Density_min.get_resources())
#print(Rulebook.Density_min.apply(cont.get_nearest_grid_points([-432432, -42343242, 4234324]), 0.0023))

a = Factories.ARBITER(cont2)
cells = a.create_cell_structure([10, 10, 10], [2, 2, 2], {'mat_density': 0.00787, 'wall_thickness': 0.2})

for cell in cells:
    result = a.apply_rules(cell, [Rulebook.Density_min], ['min'], [ExtPropCalc.CellDensity])
    print(cell, ': Grid Density > Cell Density? ', result)
