from random import randint
import json

class Container:
    def __init__(self, filename):
        self.__grid_data_length = 0
        self.__grid_data = []
        self.__infile = open(filename, 'r')
        self.__grid = json.load(self.__infile)
        pass

    ####################################################################################################################


    def __del__(self):
        self.__infile.close()

    ####################################################################################################################


    def getNearestData(self, coordinates):
        """Calculates the Euclidean distance between 'coordinates' and grid data and returns the data of the closest
        grid point"""

        data_index = randint(0, self.__grid_data_length)
        eucl_dist_prev = inf

        for i in range(self.__grid_data_length):
            eucl_dist = sqrt(sum([(a - b) ** 2 for a, b in zip(coordinates, self.__grid_data[i][1:4])]))

            if (eucl_dist < eucl_dist_prev):
                data_index = i
            eucl_dist_prev = min(eucl_dist, eucl_dist_prev)

        return self.__grid_data[data_index]

    ####################################################################################################################


    def getEnclosedData(self, minmax_coordinates):
        """Returns a list of grid data of all grid elements within 'minmax_coordinates'"""

        x_min = minmax_coordinates[0][0]
        x_max = minmax_coordinates[0][1]
        y_min = minmax_coordinates[1][0]
        y_max = minmax_coordinates[1][1]
        z_min = minmax_coordinates[2][0]
        z_max = minmax_coordinates[2][1]
        data_list = []

        for i in range(self.__grid_data_length):
            if x_min <= self.__grid_data[i][1] <= x_max and \
                                    y_min <= self.__grid_data[i][2] <= y_max and \
                                    z_min <= self.__grid_data[i][3] <= z_max:
                data_list.append(self.__grid_data[i])

        return data_list