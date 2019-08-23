from random import randint
from math import inf, sqrt
import json

class Container:
    def __init__(self, *filename):

        if filename != ():
            self._infile = open(filename[0], 'r')
            indata = json.load(self._infile)
            header = indata['header']
            self._origin = header['origin']
            self._dimensions = header['dimensions']
            self._max_index = header['max_index']
            self._grid = indata['body']
            self._grid_length = len(self._grid)
        else:
            self._infile = None
            self._grid = None
            self._grid_length = None

    def __del__(self):
        if self._infile:
            self._infile.close()

    def load_file(self, filename):
        if self._infile:
            self._infile.close()
        self._infile = open(filename, 'r')
        indata = json.load(self._infile)
        header = indata['header']
        self._origin = header['origin']
        self._dimensions = header['dimensions']
        self._max_index = header['max_index']
        self._grid = indata['body']
        self._grid_length = len(self._grid)

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

    def get_max_index(self, axis):
        """Returns the highest coordinate indices of input grid"""
        keys = {'x': 0, 'y': 1, 'z': 2}
        return self._max_index[keys[axis]]

    def get_min_index(self, axis):
        """Returns the lowest coordinate indices of input grid"""
        keys = {'x': 0, 'y': 1, 'z': 2}
        return self._origin[keys[axis]]

    def dump_data(self):
        """Returns input data as a string"""

        return json.dumps(self._grid)

    def length_of_data(self):
        """Returns length of input grid data list"""

        return self._grid_length