from numpy import inf
from math import sqrt
from ExtPropCalc import minmaxCoordinates

class Arbiter:
    def __init(self, data_container, *args):
        self.__data_container = data_container
        pass

    ####################################################################################################################


    def applyRules(self, cell, rules, priorities, calc):
        """Applies the passed rules to cell and returns a boolean.
        cell: Cell to be tested against rules.
        rules: A list of rule classes.
        priorities: A list of priorities, in which order the rules are being applied. Must be the same length as rules.
        *calc: Functions for calculating properties that are not contained in cell data directly.

        Return Values: True - Cell is within set properties. False - Cell exceeds properties
        """

        cell_minmax = minmaxCoordinates(cell.properties('location'), cell.properties('dimensions'))
        grid_data = self.__data_container.getData(cell_minmax)

        for rule in rules:
            prop = rule.getProp()
            rule.apply(prop, grid_data['prop'])

        pass

    ####################################################################################################################

    def splitCell(self, axis, cell):
        pass
