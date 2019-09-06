"""Helper functions and classes for calculations and miscellaneous tasks"""

from ExtPropCalc import Calculator


class MinMaxCoordinates(Calculator):
    """Calculates the min and max coordinates from cell location and dimensions.
    Min and Max can be calculated for any given dimensions."""

    prop = 'minmax'
    resources = ('location', 'dimensions')

    def __init__(self):
        super().__init__()

    @classmethod
    def calc(cls, *ext_resources):
        location = ext_resources[0]
        dimensions = ext_resources[1]
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

def frange(start, stop, step = 1, *decimals):
    """Implements range() generator for floats.
    start:      lower limit
    stop:       upper limit
    step:       step size (if no argument is passed, default 1)
    decimals:   round to given decimals (optional)"""

    while start < stop:
        if decimals:
            yield round(start, decimals[0])
        else:
            yield start
        start += step