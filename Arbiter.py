from numpy import inf
from math import sqrt
from ExtPropCalc import MinMaxCoordinates

class Arbiter:
    def __init__(self, data_container, *args):
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

        #cell_minmax = MinMaxCoordinates.calc([cell.properties('location'), cell.properties('dimensions')])
        grid_data = self.__data_container.getData(cell_minmax)

        rule_results = []
        for i in range(len(rules)):
            resource = rules[i].getResources()
            if calc[i] != 0:
                pcalc = calc[i]
                pcalc_resources = pcalc.getResources()
                resource_list = []
                for r in pcalc_resources:
                    resource_list.append(cell.properties(r))
                pcalc_result = pcalc.calc(resource_list)
                rule_results.append(rules[i].apply(pcalc_result, grid_data[resource]))
            else:
                rule_results.append(rules[i].apply(cell.properties(resource), grid_data[resource]))
        return rule_results

    ####################################################################################################################

    def splitCell(self, axis, cell):
        pass
