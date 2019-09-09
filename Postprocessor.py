"""Postprocessor, converts cell structure to layer slices"""

from Helpers import frange

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