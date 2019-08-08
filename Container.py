from random import randint
from math import inf, sqrt
import json

class Container:
    def __init__(self, *filename):

        if filename != ():
            self.__infile = open(filename[0], 'r')
            indata = json.load(self.__infile)
            header = indata['header']
            self.__origin = header['origin']
            self.__dimensions = header['dimensions']
            self.__grid = indata['body']
            self.__grid_length = len(self.__grid)
        else:
            self.__infile = None
            self.__grid = None
            self.__grid_length = None

    ####################################################################################################################

    def __del__(self):
        if self.__infile:
            self.__infile.close()


    ####################################################################################################################

    def load_file(self, filename):
        if self.__infile:
            self.__infile.close()
        self.__infile = open(filename, 'r')
        indata = json.load(self.__infile)
        header = indata['header']
        self.__origin = header['origin']
        self.__dimensions = header['dimensions']
        self.__grid = indata['body']
        self.__grid_length = len(self.__grid)


    ####################################################################################################################


    def get_nearest_grid_points(self, coordinates):
        """Calculates the Euclidean distance between 'coordinates' and grid data and returns the data of the closest
        grid point"""

        data_index = randint(0, self.__grid_length)
        eucl_dist_prev = inf

        for id, grid_point in self.__grid.items():
            eucl_dist = sqrt(sum([(a - b) ** 2 for a, b in zip(coordinates, grid_point["location"])]))
            if eucl_dist < eucl_dist_prev:
                data_index = id
            eucl_dist_prev = min(eucl_dist, eucl_dist_prev)

        return self.__grid[data_index]

    ####################################################################################################################


    def get_enclosed_grid_points(self, minmax_coordinates):
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

        for id, grid_point in self.__grid.items():
            if x_min <= grid_point['location'][x] <= x_max and \
                                    y_min <= grid_point["location"][y] <= y_max and \
                                    z_min <= grid_point["location"][z] <= z_max:
                data_list.append(grid_point)

        return data_list

    ####################################################################################################################


    def get_grid_points(self, minmax_coordinates):
        """Always returns grid point data. If get_enclosed_grid_points() returns empty,
        get_nearest_grid_points() returns closest data point"""

        data_list = self.get_enclosed_grid_points(minmax_coordinates)
        if not data_list:
            coords_x = (minmax_coordinates[0][0] + minmax_coordinates[0][1]) / 2
            coords_y = (minmax_coordinates[1][0] + minmax_coordinates[1][1]) / 2
            coords_z = (minmax_coordinates[2][0] + minmax_coordinates[2][1]) / 2
            coordinates = [coords_x, coords_y, coords_z]
            data_list = [self.get_nearest_grid_points(coordinates)]

        return data_list

    ####################################################################################################################

    '''
    def getData(self, minmax_coordinates, *properties):
        grid_points = self.get_grid_points(minmax_coordinates)
        grid_data = []
        for grid_point in grid_points:
            grid_point.
    '''

    def dump_data(self):
        """Returns input data as a string"""

        return json.dumps(self.__grid)

    ####################################################################################################################


    def length_of_data(self):
        """Returns length of input grid data list"""

        return self.__grid_length