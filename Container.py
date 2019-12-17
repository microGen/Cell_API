from random import randint
from math import inf, sqrt
import json

class Container:
    def __init__(self, *filename):

        self._infile = open(filename[0], 'r')
        indata = json.load(self._infile)
        self._settings = indata['settings']
        self._grid = indata['grid']
        self._grid_length = len(self._grid)

    def __del__(self):
        if self._infile:
            self._infile.close()

    def get_nearest_gridpoint(self, coordinates):
        """Calculates the Euclidean distance between 'coordinates' and grid data and returns the data of the closest
        grid point"""

        data_index = randint(0, self._grid_length)
        eucl_dist_prev = inf

        for id, grid_point in self._grid.items():
            eucl_dist = sqrt(sum([(a - b) ** 2 for a, b in zip(coordinates, grid_point["location"])]))
            if eucl_dist < eucl_dist_prev:
                data_index = id
            eucl_dist_prev = min(eucl_dist, eucl_dist_prev)

        return self._grid[data_index]

    def get_enclosed_gridpoints(self, minmax_coordinates):
        """Returns a list of grid data of all grid elements within 'minmax_coordinates'"""

        x = 0
        y = 1
        z = 2

        x_min = minmax_coordinates[0][0]
        x_max = minmax_coordinates[0][1]
        y_min = minmax_coordinates[1][0]
        y_max = minmax_coordinates[1][1]
        z_min = minmax_coordinates[2][0]
        z_max = minmax_coordinates[2][1]
        data_list = []

        for id, grid_point in self._grid.items():
            if x_min <= grid_point['location'][x] <= x_max and \
                                    y_min <= grid_point["location"][y] <= y_max and \
                                    z_min <= grid_point["location"][z] <= z_max:
                data_list.append(grid_point)

        return data_list

    def get_gridpoint_by_ID(self, ID):
        """Returns grid point with passed ID"""

        return self._grid[ID]

    def get_gridpoint_by_index(self, x_index, y_index, z_index):
        "Returns grid point by converting the X/Y/Z index into the ID and passing it to get_gridpoint_by_ID()"

        identifier = f"{x_index:06}.{y_index:06}.{z_index:06}"
        return self.get_gridpoint_by_ID(identifier)

    def get_gridpoints(self, minmax_coordinates):
        """Always returns grid point data. If get_enclosed_gridpoints() returns empty,
        get_nearest_gridpoint() returns closest data point"""

        data_list = self.get_enclosed_gridpoints(minmax_coordinates)
        if not data_list:
            coords_x = (minmax_coordinates[0][0] + minmax_coordinates[0][1]) / 2
            coords_y = (minmax_coordinates[1][0] + minmax_coordinates[1][1]) / 2
            coords_z = (minmax_coordinates[2][0] + minmax_coordinates[2][1]) / 2
            coordinates = [coords_x, coords_y, coords_z]
            data_list = [self.get_nearest_gridpoint(coordinates)]

        return data_list

    def _get_settings(self, key, axis = None):
        """Returns settings data with argument key. Method works in the background of all getter methods that access
        the settings input data."""

        index = None

        if type(axis) == str:
            keys = {'x': 0, 'y': 1, 'z': 2}
            index = keys[axis]
        elif type(axis) == int:
            index = axis

        if index is not None:
            return self._settings[key][index]
        else:
            return self._settings[key]


    def get_max_index(self, axis = None):
        """Returns the highest coordinate indices of input grid per axis.
        If no axis is given, returns all 3 indices as list"""

        return self._get_settings('max_index', axis)

    def get_min_index(self, axis = None):
        """Returns the lowest coordinate indices of input grid per axis.
        If no axis is given, returns all 3 indices as list"""

        return self._get_settings('origin', axis)

    def get_structure_dims(self, axis = None):
        """Returns initial cell structure dimensions. If no axis is given, returns all 3 dimensions as list"""

        return self._get_settings('dimensions', axis)

    def get_cell_dims(self, axis = None):
        """Returns initial cell size per axis. If no axis is given, returns all 3 dimensions as list"""

        return self._get_settings('cell_dimensions', axis)

    def get_min_cell_dimensions(self, axis = None):
        """Returns minimum permittable cell dimensions. If no axis is given, returns all 3 dimensions as list"""

        return self._get_settings('min_cell_dimensions', axis)

    def get_defaults(self):
        """Returns cell default properties"""

        return self._get_settings('default_properties')

    def dump_data(self):
        """Returns input data as a string"""

        return json.dumps(self._grid)

    def length_of_data(self):
        """Returns length of input grid data list"""

        return self._grid_length