"""Cell Framework
Copyright (c) 2019 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)

Helper functions and classes for calculations and miscellaneous tasks"""

from statistics import mean, median
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


def pick_sample(sample_set, option):
    """Handles picking of one sample out of a set.
    Supported options are min, max, arithmetic mean (amn), median (med)"""

    def prop_min(set):
        return min(set)
    def prop_max(set):
        return max(set)
    def prop_amn(set):
        return mean(set)
    def prop_med(set):
        return median(set)
    option_list = {'min': prop_min, 'max': prop_max, 'amn': prop_amn, 'med': prop_med}
    func = option_list.get(option)
    return func(sample_set)