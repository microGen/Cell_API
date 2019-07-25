from numpy import inf
from math import sqrt

class Arbiter:
    def __init(self, *args):
        pass

    ####################################################################################################################


    def fetchGridData(self, enclosed, minmax, nearest, coordinates):
        grid_data = enclosed(minmax)
        if not grid_data:
            grid_data = nearest(coordinates)

        return grid_data

    ####################################################################################################################


    def applyRules(self, cell, rules, priorities, *calc):
        """Applies the passed rules to cell and returns a boolean.
        cell: Cell to be tested against rules.
        rules: A list of rule classes.
        priorities: A list of priorities, in which order the rules are being applied. Must be the same length as rules.
        *calc: Functions for calculating properties that are not contained in cell data directly.

        Return Values: True - Cell is within set properties. False - Cell exceeds properties
        """


        pass

    ####################################################################################################################

    def splitCell(self, axis, cell):
        pass
