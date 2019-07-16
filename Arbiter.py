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
