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

    prop = 'density'
    ### CHANGE DENSITY BACK TO MAT DENSITY
    resources = ('dimensions', 'wall_thickness', 'density')

    def __init__(self):
        super().__init__()

    @classmethod
    def calc(cls, ext_resources):
        """ext_resources: dimensions, wall_thickness, mat_density"""
        #dimensions = ext_resources['dimensions']
        #wall_thickness = ext_resources[1]
        #mat_density = ext_resources[2]
        innerHexa = [i - 2*ext_resources['wall_thickness'] for i in ext_resources['dimensions']]
        outerVolume = reduce(lambda res, i: res*i, ext_resources['dimensions'])
        innerVolume = reduce(lambda res, i: res*i, innerHexa)

        return {cls.prop: (outerVolume - innerVolume) / outerVolume * ext_resources['density']}


