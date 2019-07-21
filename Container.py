from random import randint
from math import inf, sqrt
import json

class Container:
    def __init__(self, *filename):

        if filename != ():
            self.__infile = open(filename[0], 'r')
            self.__grid = json.load(self.__infile)
            self.__grid_length = len(self.__grid)
        else:
            self.__infile = None
            self.__grid = None
            self.__grid_length = None

    ####################################################################################################################

    def __del__(self):
        self.__infile.close()


    ####################################################################################################################

    def loadFile(self, filename):
        if self.__infile:
            self.__infile.close()
        self.__infile = open(filename, 'r')
        self.__grid = json.load(self.__infile)
        self.__grid_length = len(self.__grid)


    ####################################################################################################################


    def getNearestData(self, coordinates):
        """Calculates the Euclidean distance between 'coordinates' and grid data and returns the data of the closest
        grid point"""

        data_index = randint(0, self.__grid_length)
        eucl_dist_prev = inf

        for i in range(self.__grid_length):
            str_i = str(i)
            eucl_dist = sqrt(sum([(a - b) ** 2 for a, b in zip(coordinates, self.__grid[str_i]["Location"])]))

            if (eucl_dist < eucl_dist_prev):
                data_index = str_i
            eucl_dist_prev = min(eucl_dist, eucl_dist_prev)

        return self.__grid[data_index]

    ####################################################################################################################


    def getEnclosedData(self, minmax_coordinates):
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

        for i in range(self.__grid_length):
            str_i = str(i)
            if x_min <= self.__grid[str_i]['Location'][x] <= x_max and \
                                    y_min <= self.__grid[str_i]["Location"][y] <= y_max and \
                                    z_min <= self.__grid[str_i]["Location"][z] <= z_max:
                data_list.append(self.__grid[str_i])

        return data_list

    ####################################################################################################################


    def getData(self, minmax_coordinates):
        """Always returns data. If getEnclosedData() returns empty, getNearestData() returns closest data point"""

        data_list = self.getEnclosedData(minmax_coordinates)
        if data_list == []:
            coords_x = (minmax_coordinates[0][0] + minmax_coordinates[0][1]) / 2
            coords_y = (minmax_coordinates[1][0] + minmax_coordinates[1][1]) / 2
            coords_z = (minmax_coordinates[2][0] + minmax_coordinates[2][1]) / 2
            coordinates = [coords_x, coords_y, coords_z]
            data_list = [self.getNearestData(coordinates)]

        return data_list

    ####################################################################################################################


    def dumpData(self):
        """Returns input data as a string"""

        return json.dumps(self.__grid)

    ####################################################################################################################


    def lengthOfData(self):
        """Returns length of input grid data list"""

        return self.__grid_length