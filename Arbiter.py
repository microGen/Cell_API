from numpy import inf
from math import sqrt

class Arbiter:
    def __init(self):
        pass

    ####################################################################################################################


    def minmaxCoordinates(self, coordinates, dimensions):
        return_coordinates = []

        for i in range(3):
            min = coordinates[i] - dimensions[i] / 2
            max = coordinates[i] + dimensions[i] / 2
            return_coordinates.append([min, max])

        return return_coordinates

    ####################################################################################################################


    def fetchGridData(self, enclosed, minmax, nearest, coordinates):
        grid_data = enclosed(minmax)
        if not grid_data:
            grid_data = nearest(coordinates)

        return grid_data

    ####################################################################################################################


    def splitCell(self, stress_axis, cell):
        pass

    ####################################################################################################################


    def getNearestData(self, coordinates):
        """Calculates the Euclidean distance between 'coordinates' and grid data and returns the data of the closest
        grid point"""

        eucl_dist_prev = inf

        for i in range(self.__FEA_data_length):
            eucl_dist = sqrt(sum([(a - b) ** 2 for a, b in zip(coordinates, self.__FEA_data[i][1:4])]))

            if (eucl_dist < eucl_dist_prev):
                data_index = i
            eucl_dist_prev = min(eucl_dist, eucl_dist_prev)

        return self.__FEA_data[data_index]

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

        for i in range(self.__FEA_data_length):
            if x_min <= self.__FEA_data[i][1] <= x_max and \
                                    y_min <= self.__FEA_data[i][2] <= y_max and \
                                    z_min <= self.__FEA_data[i][3] <= z_max:
                data_list.append(self.__FEA_data[i])

        return data_list