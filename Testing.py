from Cell import Cell, CellFinal
import CellGeometry
from Container import Container
from Arbiter import Arbiter

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

    container_testfile = "unit_testfile.txt"
    container_test = Container(container_testfile)