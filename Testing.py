"""Unit Tests"""

#Classes
from Cell import Cell
import CellGeometry
from Container import Container
from Engine import Engine
import Rulebook

#Functions
import ExtPropCalc
import Helpers


def cell_unit_test():
    """Unit test for all class methods of Cell"""

    cell_test_id = -1
    cell_test_location = [0, 0, 0]
    cell_test_dimensions = [2, 2, 2]
    cell_test_ext_data = {'mat_density': 1, 'youngs': 100000000, 'poisson': 0.3}

    cell_test_volume = cell_test_dimensions[0] * cell_test_dimensions[1] * cell_test_dimensions[2]

    cell_test = Cell(cell_test_id, cell_test_location, cell_test_dimensions, cell_test_ext_data)

    assert cell_test.ID() == cell_test_id, "Cell ID assertion failed."
    assert cell_test.properties('location') == cell_test_location, "Cell location assertion failed."
    assert cell_test.properties('dimensions') == cell_test_dimensions, "Cell dimensions assertion failed."
    for i in range(8):
        assert type(cell_test.vertices()[i]) is CellGeometry.Vertex, "Cell vertex type assertion failed"
        #assert location of individual vertices
    for i in range(12):
        assert type(cell_test.edges()[i]) is CellGeometry.Edge, "Cell edge type assertion failed"
    for i in range(6):
        assert type(cell_test.faces()[i]) is CellGeometry.Face, "Cell face type assertion failed"
    assert cell_test.properties('volume') == cell_test_volume, "Cell volume assertion failed"
    assert cell_test.is_final() == False, "Cell state assertion 1 failed: final state reached unexpectedly"
    cell_test.set_final()
    assert cell_test.is_final() == True, "Cell state assertion 2 failed: final state not reached"

    print('Unit test passed: class Cell')

    ####################################################################################################################


def container_unit_test():
    """Unit tests for all methods of container"""

    container_testfile = "unit_testfile.json"
    container_test = Container(container_testfile)
    assert container_test.get_nearest_gridpoint([0, 0, 0]) == {'index': [0, 0, 0], 'location': [0, 0, 0], 'density': 1}, \
        "Assert getting nearest data successful failed"
    assert container_test.get_nearest_gridpoint([5, 5, 5]) == {'index': [3, 3, 3], 'location': [4, 5, 4], 'density': 5}, \
        "Assert getting nearest data unsuccessful failed"
    assert container_test.get_enclosed_gridpoints([[1, 4], [1, 4], [1, 4]]) == \
           [{'index': [1, 1, 1], 'location': [1, 1, 1], 'density': 2},\
            {'index': [2, 2, 2], 'location': [3, 4, 2], 'density': 3.14159}], \
        "Assert getting contained data successful failed"
    assert container_test.get_enclosed_gridpoints([[6, 6], [6, 6], [6, 6]]) == [], \
        "Assert getting enclosed data unsuccessful failed"
    assert container_test.get_gridpoint_by_index(0, 0, 0) == {'index': [0, 0, 0], 'location': [0, 0, 0], 'density': 1}, \
        "Assert getting gridpoint by index failed"
    assert container_test.length_of_data() == 4, \
        "Assert input data length failed"
    container_test.load_file("unit_testfile2.json")
    assert container_test.length_of_data() == 1, \
        "Assert input data length after loading different file failed"

    print('Unit test passed: class Container')

    ####################################################################################################################


def prop_calc_unit_test():
    """Unit tests for external property calculator functions"""
    sigma = 0.01
    test_density = 6.17008E-3
    calc_result = ExtPropCalc.CellDensity.calc({'dimensions': [10, 10, 10], 'wall_thickness': 2, 'mat_density': 0.00787})
    assert (test_density - sigma * test_density) <= calc_result['density']\
           <= (test_density + sigma * test_density), "Assert cell density calculation failed"

    print('Unit test passed: Properties Calculator')

    ####################################################################################################################


def rulebook_unit_test():
    """Unit tests for Rulebook"""
    ut_grid = {'location': [1, 1, 1], 'density': 0.07}
    ut_cell = Cell(0, [1, 1, 1], [1, 1, 1], {'density': 0.0699})
    assert Rulebook.Density_min.apply(ut_grid, ut_cell.properties()) == True, "Assert Rulebook.Density_min failed"
    assert Rulebook.Density_max.apply(ut_grid, ut_cell.properties()) == False, "Assert Rulebook.Density_max failed"

    print('Unit test passed: Rulebook')

    ####################################################################################################################


def helpers_unit_test():
    """Unit tests for helper functions"""
    location = [2, 3, 4]
    dimensions = [1, 7, 2]
    assert Helpers.MinMaxCoordinates.calc(location, dimensions) == [[1.5, 2.5], [-0.5, 6.5], [3, 5]], "Assert Helpers.MinMaxCoordinates failed"

    print('Unit test passed: Helpers')