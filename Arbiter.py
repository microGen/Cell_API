from numpy import inf
from math import sqrt
from statistics import mean, median
import Factories
from Helpers import MinMaxCoordinates

class Arbiter:
    def __init__(self, data_container, *args):
        self.__data_container = data_container
        self.__cell_serial_number = 0
        pass


    def create_cell_structure(self, dims, init_cell_size, cell_properties):
        """Creates initial cell structure using arguments.
        dims: [x, y, z] - maximum dimensions, origin is [0, 0, 0]
        init_cell_size: [x, y, z] - initial cell size
        cell_properties: dictionary - properties transmitted by the cell data input file"""

        cells = []
        for x in range(0, dims[0]+1, init_cell_size[0]):
            for y in range(0, dims[1]+1, init_cell_size[1]):
                for z in range(0, dims[2]+1, init_cell_size[2]):
                    cell = Factories.CELL(self.__cell_serial_number, [x, y, z], init_cell_size, cell_properties, False)
                    cells.append(cell)
                    self.__cell_serial_number += 1
        return cells

    ####################################################################################################################


    def apply_rules(self, cell, rules, prop_options, calc):
        """Applies rules from rulebook to determine whether a cells properties are within specifications.
        cell: current cell to be examined
        rules: list of rules to apply for examination of cell
        prop_options: list of options of the same length as rules to set whether min/max/mean/median of applicable
            grid data is to be used as input for the rule
        calc: optional calculator. If a property is not directly supplied by cell data, a calculator can be applied for
            necessary calculations. Must be a list of the same length as rules. If no calculator is needed, the list
            must be 0"""

        # Handles choice of options for extraction of grid point properties.
        # Supported options are min, max, arithmetic mean (amn), median (med)
        def calc_prop_opt(properties, option):
            def prop_min(props):
                return min(props)
            def prop_max(props):
                return max(props)
            def prop_amn(props):
                return mean(props)
            def prop_med(props):
                return median(props)
            option_list = {'min': prop_min, 'max': prop_max, 'amn': prop_amn, 'med': prop_med}
            func = option_list.get(option)
            return func(properties)

        cell_minmax = MinMaxCoordinates.calc(cell.properties('location'), cell.properties('dimensions'))
        grid_points = self.__data_container.get_grid_points(cell_minmax)

        rule_results = []

        for i in range(len(rules)):
            # Grid points should only get resource lists from rules as they must already contain the data that the rule
            # compares the cell to.
            rule_resources = rules[i].get_resources()

            # Choose how to get resource data from cell. If property calculator exists for rule, the resource list is
            # generated by calling its resource getter method. The cell's properties are passed to the calculator, which
            # generates the final property to be compared with grid data. Otherwise, cell properties are pulled by
            # calling the rule's getter.
            if calc[i] != 0:
                calc_resources = calc[i].get_resources()
                cell_properties = {cr: cell.properties(cr) for cr in calc_resources}
                cell_resources = calc[i].calc(cell_properties)
            else:
                calc_resources = rule_resources
                cell_resources = {cr: cell.properties(cr) for cr in calc_resources}

            # Get property list from the grid...
            grid_resource_list = []
            for grid_point in grid_points:
                grid_resource = {rr: grid_point[rr] for rr in rule_resources}
                grid_resource_list.append(grid_resource)
            # ...and extract the min / max / mean / median value from list
            grid_resources = {}
            for resource in rule_resources:
                grid_data = [gr[resource] for gr in grid_resource_list]
                grid_resources.update({resource: calc_prop_opt(grid_data, prop_options[i])})
            rule_results.append(rules[i].apply(grid_resources, cell_resources))
            #print('Grid resources: ', grid_resources, ' Cell resources: ', cell_resources)

        return rule_results

    ####################################################################################################################


    def split_cell(self, axis, cell):
        pass
