"""Unit Tests"""

#Classes
from Cell import Cell, CellFinal
import CellGeometry
from Container import Container
from Arbiter import Arbiter

#Functions
import ExtPropCalc


def cell_unit_test():
    """Unit test for all class methods of Cell"""

    cell_test_id = -1
    cell_test_location = [0, 0, 0]
    cell_test_dimensions = [2, 2, 2]
    cell_test_ext_data = {'density': 1, 'youngs': 100000000, 'poisson': 0.3}

    ctm_xmin = cell_test_location[0] - cell_test_dimensions[0] / 2
    ctm_xmax = cell_test_location[0] + cell_test_dimensions[0] / 2
    ctm_ymin = cell_test_location[1] - cell_test_dimensions[1] / 2
    ctm_ymax = cell_test_location[1] + cell_test_dimensions[1] / 2
    ctm_zmin = cell_test_location[2] - cell_test_dimensions[2] / 2
    ctm_zmax = cell_test_location[2] + cell_test_dimensions[2] / 2
    cell_test_minmax = [[ctm_xmin, ctm_xmax], [ctm_ymin, ctm_ymax], [ctm_zmin, ctm_zmax]]
    cell_test_volume = cell_test_dimensions[0] * cell_test_dimensions[1] * cell_test_dimensions[2]

    cell_test = Cell(cell_test_id, cell_test_location, cell_test_dimensions, cell_test_ext_data)

    assert cell_test.ID() == cell_test_id, "Cell ID assertion failed."
    assert cell_test.location() == cell_test_location, "Cell location assertion failed."
    assert cell_test.dimensions() == cell_test_dimensions, "Cell dimensions assertion failed."
    assert cell_test.minmax() == cell_test_minmax, "Cell min/max coordinates assertion failed"
    for i in range(8):
        assert type(cell_test.vertices()[i]) is CellGeometry.Vertex, "Cell vertex type assertion failed"
        #assert location of individual vertices
    for i in range(12):
        assert type(cell_test.edges()[i]) is CellGeometry.Edge, "Cell edge type assertion failed"
    for i in range(6):
        assert type(cell_test.faces()[i]) is CellGeometry.Face, "Cell face type assertion failed"
    assert cell_test.volume() == cell_test_volume, "Cell volume assertion failed"
    assert cell_test.coreProperties() == {'Location': cell_test_location,\
                                          'Dimensions': cell_test_dimensions,\
                                          'Volume': cell_test_volume}, "Cell core properties assertion failed"
    assert cell_test.isFinal() == False, "Cell state assertion 1 failed: final state reached unexpectedly"
    cell_test.setFinal()
    assert cell_test.isFinal() == True, "Cell state assertion 2 failed: final state not reached"

    print('Unit test passed: class Cell')

    ####################################################################################################################


def container_unit_test():
    """Unit tests for all methods of container"""

    container_testfile = "unit_testfile.json"
    container_test = Container(container_testfile)
    assert container_test.getNearestData([0, 0, 0]) == {'Location': [0, 0, 0], 'Density': 1}, \
        "Assert getting nearest data successful failed"
    assert container_test.getNearestData([5, 5, 5]) == {'Location': [4, 5, 4], 'Density': 5}, \
        "Assert getting nearest data unsuccessful failed"
    assert container_test.getEnclosedData([[1, 4], [1, 4], [1, 4]]) == [{'Location': [1, 1, 1], 'Density': 2},\
                                                                        {'Location': [3, 4, 2], 'Density': 3.14159}], \
        "Assert getting contained data successful failed"
    assert container_test.getEnclosedData([[6, 6], [6, 6], [6, 6]]) == [], \
        "Assert getting enclosed data unsuccessful failed"
    assert container_test.lengthOfData() == 4, \
        "Assert input data length failed"
    container_test.loadFile("unit_testfile2.json")
    assert container_test.lengthOfData() == 1, \
        "Assert input data length after loading different file failed"

    print('Unit test passed: class Container')

    ####################################################################################################################


def prop_calc_unit_test():
    """Unit tests for external properties calculators"""
    sigma = 0.01
    test_density = 6.17008E-3
    assert (test_density - sigma * test_density) <= ExtPropCalc.cellDensity([10, 10, 10], 2, 0.00787)\
           <= (test_density + sigma * test_density), "Assert cell density calculation failed"

    print('Unit test passed: properties calculator')