"""
Functions for calculating properties like density that are not contained in cell data directly.
Define functions here in order to implement new features.
Works in conjunction with the rules of Rulebook.py
"""

from functools import reduce
from Rulebook import PropRule


class CellDensity(PropRule):
    """Calculates the resulting density of the cell when void is subtracted from the outer wall.
    Air density is neglected."""

    def __init__(self):
        super().__init__('density', 'dimensions', 'wall_thickness', 'mat_density')

    def calc(self, dimensions, wall_thickness, mat_density):
        innerHexa = [i - 2*wall_thickness for i in dimensions]
        outerVolume = reduce(lambda res, i: res*i, dimensions)
        innerVolume = reduce(lambda res, i: res*i, innerHexa)

        return (outerVolume - innerVolume) / outerVolume * mat_density


class MinMaxCoordinates(PropRule):
    """Calculates the min and max coordinates from cell location and dimensions.
    Min and Max can be calculated for any given dimensions."""

    def __init__(self):
        super().__init__('minmax', 'location', 'dimensions')

    def calc(self, location, dimensions):
        if (type(location) is int or type(location) is float) and (type(dimensions) is int or type(dimensions) is float):
            min_location = location - dimensions / 2
            max_location = location + dimensions / 2
            minmax_coordinates = [min_location, max_location]
        else:
            minmax_coordinates = []
            for i in range(len(location)):
                min_location = location[i] - dimensions[i] / 2
                max_location = location[i] + dimensions[i] / 2
                minmax_coordinates.append([min_location, max_location])
        return minmax_coordinates