"""Postprocessor, converts cell structure to layer slices"""

from Helpers import frange, MinMaxCoordinates

class Postprocessor:

    def __init__(self, engine_instance, slice_thickness):
        self._engine = engine_instance
        data_container = self._engine.get_container()
        z_max = data_container.get_structure_dims('z')
        self._layer_num = z_max / slice_thickness
        self._layers = [round(l, 8) for l in frange(0, z_max, slice_thickness)]
        self._z = z_max

    def test(self):
        print('TEST POSTPROCESSOR: Layers: ', self._layer_num, ' Z Max: ', self._z)
        print('Layers: ', self._layers)
        for cell in self._engine.get_cells():
            print('Cell: ', cell.ID(), cell.geometry('location'), cell.geometry('dimensions'))
        print('\nFINALS:')
        for cell in self._engine.get_cells(True):
            if self._check_cell_z(cell, 0.3):
                print('Cell: ', cell.ID(), cell.geometry('location'), cell.geometry('dimensions'))
            else:
                print('NOT: ', cell.ID(), cell.geometry('location'), cell.geometry('dimensions'))

    def _check_cell_z(self, cell, z_slice):
        cell_z = MinMaxCoordinates.calc(cell.geometry('location'), cell.geometry('dimensions'))[2]
        if cell_z[0] <= z_slice <= cell_z[1]:
            return True
        else:
            return False