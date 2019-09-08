import Factories
from FileIO import FileIO
import Testing
import Rulebook
import ExtPropCalc
import Helpers
from Engine import Engine

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

#print(ExtPropCalc.CellDensity.get_resources_grid())
#print(Rulebook.Density_min.get_resources_grid())
#print(Rulebook.Density_min.apply(cont.get_nearest_gridpoint([-432432, -42343242, 4234324]), 0.0023))

eng = Factories.ENGINE(cont4)
#eng.create_cell_structure([10, 10, 10], [5, 5, 5], {'mat_density': 0.00787, 'wall_thickness': 0.2})
eng.create_cell_structure()

rules = [Rulebook.Density_max]

calc = ExtPropCalc.CellDensity
calc_resources = calc.get_resources_cell()

eng.evolve_cell_structure(6, rules, ['min'], [calc], False)

'''
# initial cells
cells = eng.get_cells()
outfile_name = f"cell_structure_base.txt"
outfile = open(outfile_name, 'w')
for c in cells:
    cell_properties = {cr: c.properties(cr) for cr in calc_resources}
    cell_resources = calc.calc(cell_properties)
    gridpoints = eng._get_gridpoints(c)
    gp_density = [gp['density'] for gp in gridpoints]
    single_gp = Helpers.pick_sample(gp_density, 'min')
    outstring = f"ID: {c.ID()}\tfinal: {c.is_final()}\tlocation: {c.geometry('location')}\tdimensions: {c.geometry('dimensions')}\n"
    out_density = f"Cell density: {cell_resources}\tgridpoint density: {single_gp}\n"
    outfile.write(outstring)
    outfile.write(out_density)
outfile.close()


# evolving cell structure
for i in range(iterations):
    cell_max_index = eng.next_cell_serial_num()
    cells = eng.get_cells()
    print(f'\nIteration {i}')
    for cell in cells[:cell_max_index]:
        result = eng.apply_rules(cell, rules, ['min'], [ExtPropCalc.CellDensity])
        #print('\n')
        #print(cell, ' ID: ', cell.ID(), ': Grid Density > Cell Density? ', result)
        for rule in rules:
            gradient = eng.gridpoint_gradient(cell, rule)
            #print('Gradient: ', gradient)
        gradient = gradient[0]
        result0 = result[0]
        cells_after_split = eng.split_cell(cell, result0, gradient)

    outfile_name = f"cell_structure{i:02}.txt"
    outfile = open(outfile_name, 'w')
    #print('\nCells after split ', i, ':')
    for c in cells:
        cell_properties = {cr: c.properties(cr) for cr in calc_resources}
        cell_resources = calc.calc(cell_properties)
        gridpoints = eng._get_gridpoints(c)
        gp_density = [gp['density'] for gp in gridpoints]
        single_gp = Helpers.pick_sample(gp_density, 'min')
        outstring = f"ID: {c.ID()}\tfinal: {c.is_final()}\tlocation: {c.geometry('location')}\tdimensions: {c.geometry('dimensions')}\n"
        out_density = f"Cell density: {cell_resources}\tgridpoint density: {single_gp}\n"
        outfile.write(outstring)
        outfile.write(out_density)
        #print('ID: ', c.ID(), '\tfinal: ', c.is_final(), '\tlocation: ', c.geometry('location'), '\tdimensions: ', c.geometry('dimensions'))
    outfile.close()

    #for c in eng.get_cells():
    #    print(f'Cell IDs old: {c.ID()}')
    print('\nBefore sorting: ')
    for c in eng.get_cells():
        print('Cell ID: ', c.ID(), ' Final: ', c.is_final())
    print('Finals: ')
    for c in eng.get_cells(final = True):
        print('Final Cell ID: ', c.ID(), ' Final: ', c.is_final())


    eng.sort_cells()
    print('After sorting: ')
    for c in eng.get_cells():
        print('Cell ID: ', c.ID(), ' Final: ', c.is_final())
    print('Finals: ')
    for c in eng.get_cells(final = True):
        print('Final Cell ID: ', c.ID(), ' Final: ', c.is_final())


    #for c in eng.get_cells():
    #    print(f'Cell IDs new: {c.ID()}')
'''
