import Factories
from FileIO import FileIO
import Testing
import Rulebook
import ExtPropCalc
import Helpers
from Engine import Engine
from Postprocessor import Postprocessor

debug_cell = False
debug_json = False
debug_rules = False

print('Testing stage for Cell API\n')

Testing.cell_unit_test()
#Testing.container_unit_test()
Testing.prop_calc_unit_test()
Testing.rulebook_unit_test()
Testing.helpers_unit_test()

loc = [1, 1, 1]
dim = [2, 2, 2]
iterations = 6

c = Factories.CELL(3, loc, dim, {'mat_density': 0.00787, 'wall_thickness': 0.2}, False)
#cont0 = Factories.CONTAINER("json_test_input.txt")
#cont1 = Factories.CONTAINER("grid_data.json")
#cont2 = Factories.CONTAINER("grid_data_2.json")
#cont3 = Factories.CONTAINER("grid_data_3.json")
cont4 = Factories.CONTAINER("grid_data_4.json")

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
    print('Nearest Data:\t\t', cont.get_nearest_gridpoint([-432432, -42343242, 4234324]))
    print('Enclosed Data:\t\t', cont.get_enclosed_gridpoints([[4, 5], [4, 5], [4, 5]]))
    print('All Data:\t\t\t', cont.get_gridpoints([[4, 5], [4, 5], [4, 5]]))
    print('Data fields:\t\t', cont.length_of_data())

if debug_rules:
    print(c.properties('dimensions'))
    print('prop:', ExtPropCalc.CellDensity.get_prop(), 'ressources: ', ExtPropCalc.CellDensity.get_resources_grid())
    dens = ExtPropCalc.CellDensity.calc(c.properties('dimensions'), 0.2, c.properties('mat_density'))
    print('Nearest Data:\t\t', cont.get_nearest_gridpoint([-432432, -42343242, 4234324]))
    print(dens)
    print(Rulebook.Density_min.get_prop())
    print(Rulebook.Density_min.apply(cont.get_nearest_gridpoint([-432432, -42343242, 4234324]), dens))

eng = Factories.ENGINE(cont4)
eng.create_cell_structure()

rules = [Rulebook.Density_max, Rulebook.Shell_Dist]

calc = ExtPropCalc.CellDensity
calc_resources = calc.get_resources_cell()


eng.evolve_cell_structure(6, rules, ['min', 'amn'], [calc, 0], False)
eng.extend_properties([calc])
export = eng.export_cells('finals')
export_string = eng.export_json_str(export)

export_file = open('./debug_output/Cell_export.json', 'w')
export_file.write(export_string)
export_file.close()

#eng.test()

pp = Postprocessor(eng, 0.1)
pp.test()