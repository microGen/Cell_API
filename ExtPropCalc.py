"""
Functions for calculating properties like density that are not contained in cell data directly.
Define functions here in order to implement new features.
Works in conjunction with the rules of Rulebook.py
"""

from functools import reduce

def cellDensity(dimensions, wall_thickness, mat_density):
    """Calculates the resulting density of the cell when void is subtracted from the outer wall.
    Air density is neglected."""

    innerHexa = [i - 2*wall_thickness for i in dimensions]
    outerVolume = reduce(lambda res, i: res*i, dimensions)
    innerVolume = reduce(lambda res, i: res*i, innerHexa)

    return (outerVolume - innerVolume) / outerVolume * mat_density