"""Unit Tests"""

#Classes
import Factories
import CellGeometry
import Rulebook

#Functions
import ExtPropCalc
import Helpers


def cell_unit_test():
    """Unit test for all class methods of Cell"""

    print('Unit test: Class Cell...')
    cell_test_id = -1
    cell_test_location = [0, 0, 0]
    cell_test_dimensions = [2, 2, 2]
    cell_test_vertloc = [[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]]
    cell_test_ext_data = {'mat_density': 1, 'youngs': 100000000, 'poisson': 0.3}

    cell_test_volume = cell_test_dimensions[0] * cell_test_dimensions[1] * cell_test_dimensions[2]

    cell_test = Factories.cell(cell_test_id, cell_test_location, cell_test_dimensions, cell_test_ext_data)

    assert cell_test.ID() == cell_test_id, "ID failed"
    assert cell_test.properties('location') == cell_test_location, "location failed."
    assert cell_test.properties('dimensions') == cell_test_dimensions, "dimensions failed."
    for i in range(8):
        assert type(cell_test.vertices()[i]) is CellGeometry.Vertex, "vertex type failed"
        vtest = cell_test.vertices(i)
        assert vtest.get_location() == cell_test_vertloc[i], "vertex location failed"
    for i in range(12):
        assert type(cell_test.edges()[i]) is CellGeometry.Edge, "edge type failed"
    for i in range(6):
        assert type(cell_test.faces()[i]) is CellGeometry.Face, "face type failed"
    assert cell_test.properties('volume') == cell_test_volume, "volume failed"
    assert cell_test.is_final() == False, "final state failed: reached unexpectedly"
    cell_test.set_final()
    assert cell_test.is_final() == True, "final state failed: not reached"

    print('passed.')

    ####################################################################################################################


def container_unit_test():
    """Unit tests for all methods of container"""

    print('Unit test: Class Container...')
    container_testfile = "unit_testfile.json"
    container_test = Factories.container(container_testfile)
    assert container_test.get_nearest_gridpoint([0, 0, 0]) == {'index': [0, 0, 0], 'location': [0, 0, 0], 'density': 1}, \
        "getting nearest data successful failed"
    assert container_test.get_nearest_gridpoint([5, 5, 5]) == {'index': [3, 3, 3], 'location': [4, 5, 4], 'density': 5}, \
        "getting nearest data unsuccessful failed"
    assert container_test.get_enclosed_gridpoints([[1, 4], [1, 4], [1, 4]]) == \
           [{'index': [1, 1, 1], 'location': [1, 1, 1], 'density': 2},\
            {'index': [2, 2, 2], 'location': [3, 4, 2], 'density': 3.14159}], \
        "getting contained data successful failed"
    assert container_test.get_enclosed_gridpoints([[6, 6], [6, 6], [6, 6]]) == [], \
        "getting enclosed data unsuccessful failed"
    assert container_test.get_gridpoint_by_index(0, 0, 0) == {'index': [0, 0, 0], 'location': [0, 0, 0], 'density': 1}, \
        "getting gridpoint by index failed"
    assert container_test.length_of_data() == 4, \
        "input data length failed"

    print('passed.')

    ####################################################################################################################


def prop_calc_unit_test():
    """Unit tests for external property calculator functions"""

    print('Unit test: Class ExtPropCalc.CellDensity...')
    sigma = 0.01
    test_density = 6.17008E-3
    calc_result = ExtPropCalc.CellDensity.calc({'dimensions': [10, 10, 10], 'wall_thickness': 2, 'mat_density': 0.00787})
    assert (test_density - sigma * test_density) <= calc_result['density']\
           <= (test_density + sigma * test_density), "cell density calculation failed"

    print('passed.')

    ####################################################################################################################


def rulebook_unit_test():
    """Unit tests for Rulebook"""

    print('Unit test: Classes Rulebook.Density_min and Rulebook.Density_max...')
    ut_grid = {'location': [1, 1, 1], 'density': 0.07}
    ut_cell = Factories.cell(0, [1, 1, 1], [1, 1, 1], {'mat_density': 0.07, 'wall_thickness': 0.4})
    assert Rulebook.Density_min.apply(ut_grid, ut_cell.properties()) == True, "Rulebook.Density_min failed"
    assert Rulebook.Density_max.apply(ut_grid, ut_cell.properties()) == False, "Rulebook.Density_max failed"

    print('passed.')

    ####################################################################################################################


def helpers_unit_test():
    """Unit tests for helper functions"""

    print('Unit test: Class Helpers.MinMaxCoordinates...')
    location = [2, 3, 4]
    dimensions = [1, 7, 2]
    assert Helpers.MinMaxCoordinates.calc(location, dimensions) == [[1.5, 2.5], [-0.5, 6.5], [3, 5]], "Helpers.MinMaxCoordinates failed"

    print('passed.')