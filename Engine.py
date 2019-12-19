from numpy import inf
from json import dumps
from math import ceil
from random import randint
from statistics import mean, median
from Helpers import MinMaxCoordinates, frange, pick_sample
import Factories


class Engine:
    def __init__(self, data_container):
        self._data_container = data_container
        self._cell_serial_number = 0
        self._cells = []
        self._cells_final = []
        self._gridpoint_ID = lambda x, y, z: str(f"{x:06}.{y:06}.{z:06}")
        pass

    def next_cell_serial_num(self):
        """Returns the first free serial number in list of cells"""

        return self._cell_serial_number

    def create_cell_structure(self, dims = None, init_cell_size = None, cell_properties = None):
        """Creates initial cell structure using arguments.
        dims: [x, y, z] - maximum dimensions, origin is [0, 0, 0]
        init_cell_size: [x, y, z] - initial cell size
        cell_properties: dictionary - properties transmitted by the cell data input file"""

        if dims == None:
            dims = self._data_container.get_structure_dims()
        if init_cell_size == None:
            init_cell_size = self._data_container.get_cell_dims()
        if cell_properties == None:
            cell_properties = self._data_container.get_defaults()

        if len(self._cells) > 0:
            self._cells.clear()
        for x in frange(init_cell_size[0]/2, dims[0], init_cell_size[0], 8):
            for y in frange(init_cell_size[1]/2, dims[1], init_cell_size[1], 8):
                for z in frange(init_cell_size[2]/2, dims[2], init_cell_size[2], 8):
                    cell = Factories.cell(self._cell_serial_number, [x, y, z], init_cell_size, cell_properties)
                    self._cells.append(cell)
                    self._cell_serial_number += 1
        return self._cells

    def get_cells(self, final = False, *ID):
        """Returns list of cells if no ID is given, else returns cell of given ID. If no cell exists with given ID,
        returns None type"""

        if not final:
            cell_list = self._cells
        else:
            cell_list = self._cells_final

        if not ID:
            return cell_list
        else:
            ID = ID[0]
            for cell in cell_list:
                if cell.ID() == ID:
                    return cell
            return None

    def get_container(self):
        """Returns data container that was passed during instantiation"""
        return self._data_container

    def apply_rules(self, cell, rules, prop_options):
        """Applies rules from rulebook to determine whether a cells properties are within specifications.
        cell: current cell to be examined
        rules: list of rules to apply for examination of cell
        prop_options: list of options of the same length as rules to set whether min/max/mean/median of applicable
            grid data is to be used as input for the rule. Inputs: 'min', 'max', 'amn', 'med'
        """

        # Get grid points with coordinates within - or if not available, closest to - cell
        gridpoints = self._get_gridpoints(cell)
        rule_results = []
        for i in range(len(rules)):
            # Grid points should only get resource lists from rules as they must already contain the data that the rule
            # compares the cell to.
            rule_resources_grid = rules[i].get_resources_grid()
            #self.gridpoint_gradient(gridpoints, rule_resources_grid)
            rule_resources_cell = rules[i].get_resources_cell()

            # get cell properties by calling the rule's getter.
            calc_resources = rule_resources_cell
            cell_resources = {cr: cell.properties(cr) for cr in calc_resources}

            # Get property list from the grid...
            grid_resource_list = []
            for grid_point in gridpoints:
                grid_resource = {rr: grid_point[rr] for rr in rule_resources_grid}
                grid_resource_list.append(grid_resource)
            # ...and extract the min / max / mean / median value from list
            grid_resources = {}
            for resource in rule_resources_grid:
                grid_data = [gr[resource] for gr in grid_resource_list]
                grid_resources.update({resource: pick_sample(grid_data, prop_options[i])})
            rule_results.append(rules[i].apply(grid_resources, cell_resources))
            #print('Grid resources: ', grid_resources, ' Cell resources: ', cell_resources)

        return rule_results

    def gridpoint_gradient(self, cell, rule, *sample_width):
        """Returns a list of gradients in X/Y/Z direction for passed gridpoints. If multiple gridpoints are passed,
        the central one serves as a basis for gradient calculation. Step width sets the offset of sample points.
        Gradient is calculated from 3 sample points: center and center +- sample_width, averaged. If sample width is not
        set, it reverts to default of 1"""

        gridpoints = self._get_gridpoints(cell)
        properties = [p for p in rule.get_resources_grid()]
        orientation = [o for o in rule.get_orientation()]

        if sample_width:
            sample_width = sample_width[0]
        else:
            sample_width = 1
        min_index = self._data_container.get_min_index
        max_index = self._data_container.get_max_index
        # limit the lower and upper indices for the gradient to the grid indices
        limit_lower = lambda cp, sw, ax: cp-sw if (cp-sw >= min_index(ax)) else min_index(ax)
        limit_upper = lambda cp, sw, ax: cp+sw if (cp+sw <= max_index(ax)) else max_index(ax)

        # list gridpoint indices...
        gridpoint_indices = []
        for gp in gridpoints:
            gridpoint_indices.append(gp['index'])
        # ...and extract the median index...
        mid_gp_index = ceil(len(gridpoint_indices) / 2) - 1
        # ...to get the median gridpoint ID
        gradient_base = gridpoint_indices[mid_gp_index]
        # gradient_base_ID = self._gridpoint_ID(*list(gradient_base.values()))

        gradient = []
        for i in range(len(properties)):
            p = properties[i]
            o = orientation[i]
            gradient_list = []
            for axis, index in gradient_base.items():
                # gradient for current axis
                gradient_axis = gradient_base
                # get the lower gridpoint on current axis
                index_lower = limit_lower(index, sample_width, axis)
                gradient_axis[axis] = index_lower
                gradient_lower_ID = self._gridpoint_ID(*list(gradient_axis.values()))
                gridpoint_lower = self._data_container.get_gridpoint_by_ID(gradient_lower_ID)
                # get the upper gridpoint on current axis
                index_upper = limit_upper(index, sample_width, axis)
                gradient_axis[axis] = index_upper
                gradient_upper_ID = self._gridpoint_ID(*list(gradient_axis.values()))
                gridpoint_upper = self._data_container.get_gridpoint_by_ID(gradient_upper_ID)
                # assemble list of property gradients for current axis
                gradient_item = (gridpoint_upper[p] - gridpoint_lower[p]) / 2
                gradient_list.append(gradient_item)
            gradient.append([gradient_list, o])
        return gradient

    def _get_gridpoints(self, cell):
        """Returns a list of gridpoints that either are located in the space occupied by the passed cell or
        - if no gridpoint is found within the cell's bounds, the closest gridpoint. Return data type is always list."""
        cell_minmax = MinMaxCoordinates.calc(cell.properties('location'), cell.properties('dimensions'))
        return self._data_container.get_gridpoints(cell_minmax)

    def split_cell(self, cell, rule_result, property_gradient):
        """If command is true, cell is split along or across gradient, depending on the rule setting. In order to split
        the cell, core properties are extracted and used as base for the new cells."""

        gradient = property_gradient[0]
        orientation = property_gradient[1]

        if rule_result:
            # convert cell to final cell
            cell.set_final()
            #self._cells_final.append(cell)
            #del self._cells[cell.ID()]
            return cell
        else:
            # split cell along / across gradient and get minimum cell size along split axis
            split_axis = self._create_split_plane(cell.properties('dimensions'), gradient, orientation, 'axis', ortho = True)
            sa_min_cell_dim = self._data_container.get_min_cell_dimensions(split_axis)
            # get all necessary data to create sub cells
            cell_ext_data = cell.ext_properties()
            cell_loc = cell.geometry('location')
            cell_dims = cell.geometry('dimensions')
            cell_id = cell.ID()
            # calculate dimensions of sub cells
            new_dims = cell_dims.copy()
            new_dims[split_axis] /= 2
            offset = new_dims[split_axis] / 2
            # if minimum cell dimension is reached, abort split operation
            if new_dims[split_axis] <= sa_min_cell_dim:
                cell.set_final()
                #self._cells_final.append(cell)
                #del self._cells[cell_id]
                return cell
            else:
                # calculate locations for sub cells
                new_loc_0 = cell_loc.copy()
                new_loc_0[split_axis] -= offset
                new_loc_1 = cell_loc.copy()
                new_loc_1[split_axis] += offset
                # create sub cells
                cell_n0 = Factories.cell(cell_id, new_loc_0, new_dims, cell_ext_data)
                cell_n1 = Factories.cell(self._cell_serial_number, new_loc_1, new_dims, cell_ext_data)
                self._cell_serial_number += 1
                old_cell_index = self._cells.index(cell)
                self._cells[old_cell_index] = cell_n0
                #self._cells[cell_id] = cell_n0
                self._cells.append(cell_n1)
                return [cell_n0, cell_n1]

    def _create_split_plane(self, cell_dimensions, gradient, orientation, return_format, ortho = True):
        """Finds greatest or smallest gradient according to orientation settings and builds a plane perpendicular to
        gradient axis. If argument ortho is true and the cell would be split across the smallest dimension, the next
        greatest/smallest gradient is used if both of the other cell dimensions are equal. Else, the split plane is
        built across the greatest dimension."""

        build_plane = lambda grad_index: list(filter(lambda axis: axis != grad_index, range(3)))

        gradient_index = self._find_index(gradient, orientation)
        plane = build_plane(gradient_index)

        if ortho:
            gradient_index = self._make_orthotropic(cell_dimensions, plane, gradient, gradient_index)
            plane = build_plane(gradient_index)

        '''
        plane_dims = list(map(lambda axis: cell_dimensions[axis], plane))

        if cell_dimensions[gradient_index] <= min(plane_dims):
            if plane_dims[0] == plane_dims[1]:
                # get next greatest gradient if both other axis' of cell are equal
                gradient_index_max = find_index(gradient, 'orthogonal')
                gradient_index_min = find_index(gradient, 'parallel')
                med_axis = lambda axis: axis != gradient_index_min and axis != gradient_index_max
                gradient_index = list(filter(med_axis, range(3)))[0]
            else:
                # get greatest dimension of cell, as else, a very slender cell will be generated
                gradient_index = cell_dimensions.index(max(cell_dimensions))
            plane = build_plane(gradient_index)
        '''
        # either return axis across which to split cell or return split plane
        return_format = return_format.lower()
        if return_format == 'axis':
            return gradient_index
        elif return_format == 'plane':
            return plane
        else:
            # future development?
            pass

    def _make_orthotropic(self, cell_dims, proto_plane, grad, grad_index):
        """Returns a split plane that splits the cell across the greatest dimension if split plane was built across a
        lesser dimension. Else returns the passed split plane. Attempts to create a cell structure that does not stray
        too much from orthotropic geometric properties."""

        plane_dims = list(map(lambda axis: cell_dims[axis], proto_plane))

        if cell_dims[grad_index] <= min(plane_dims):
            if plane_dims[0] == plane_dims[1]:
                # get next greatest gradient if both other axis' of cell are equal
                grad_index_max = self._find_index(grad, 'orthogonal')
                grad_index_min = self._find_index(grad, 'parallel')
                med_axis = lambda axis: axis != grad_index_min and axis != grad_index_max
                grad_index = list(filter(med_axis, range(3)))[0]
            else:
                # get greatest dimension of cell, as else, a very slender cell might be generated
                grad_index = cell_dims.index(max(cell_dims))
        return grad_index

    def _find_index(self, coord_sys, direction):
        """Choose split axis according to orientation given by rules"""
        cs = [abs(axis) for axis in coord_sys]
        if direction == 'orthogonal':
            # Split across gradient
            index = cs.index(max(cs))
        elif direction == 'parallel':
            # Split along gradient
            index = cs.index(min(cs))
        else:
            # If no orientation of split available, randomly choose an axis
            index = randint(0, 3)
        return index

    def sort_cells(self):
        """Move final cells from prototype to final list"""

        self._cells_final.extend([cell for cell in self._cells if cell.is_final()])
        self._cells = [cell for cell in self._cells if not cell.is_final()]

    def evolve_cell_structure(self, iterations, rules, rule_options, finalize_remaining = True):
        """Evolve cell structure with given settings:
        iterations: Number of iterations the algorithm has to run through optimisation
        rules: List of rules for optimisation
        rule_options: Choose gridpoints with min/max/median/mean properties for rule. List of same length as rules
        finalize_remaining (default: True): if after passing evolution iterations some cells are still prototypical,
            also set their state as final and move them to final list"""

        for i in range(iterations):
            cell_max_index = self.next_cell_serial_num()
            for cell in self._cells[:cell_max_index]:
                rule_results = self.apply_rules(cell, rules, rule_options)
                property_gradients = []
                for rule in rules:
                    property_gradients.append(self.gridpoint_gradient(cell, rule))
                #implement feature to single out rule results
                rule_result = rule_results[0]
                property_gradient = property_gradients[0][0]
                self.split_cell(cell, rule_result, property_gradient)
            self.sort_cells()

        if finalize_remaining:
            for cell in self._cells:
                cell.set_final()
            self.sort_cells()

        # logging and debugging
        debug = True
        if debug:
            outfile = open('./debug_output/evolution_result.txt', 'w')
            outfile.write('Prototypes:\n')
            for c in self._cells:
                outfile.write(f"ID:\t{c.ID():4}\t/\tlocation:\t{c.geometry('location'):}\t/\tdimensions:\t{c.geometry('dimensions')}\n")
            outfile.write('\nFinals:\n')
            for c in self._cells_final:
                outfile.write(f"ID:\t{c.ID():4}\t/\tlocation:\t{c.geometry('location')}\t/\tdimensions:\t{c.geometry('dimensions')}\n")
            outfile.close()

    def export_cells(self, type, *cell_ID):
        """Export cells as dictionary.
        type: argument 'prototype' or 'final' returns either cells from prototype or final set
        *cell: optional arguments return cell(s) with passed ID(s)"""

        if type == 'prototype':
            final_state = False
            cell_list = self._cells
        else:
            final_state = True
            cell_list = self._cells_final

        if cell_ID:
            cell_list = [self.get_cells(final_state, cell_ID[0])]

        cell_export = {}
        for cell in cell_list:
            cell_ID = cell.ID()
            cell_geometry = cell.geometry()
            cell_properties = cell.ext_properties()
            del cell_geometry['vertices']
            del cell_geometry['edges']
            del cell_geometry['faces']
            cell_data = {cell_ID: {'geometry': cell_geometry, 'properties': cell_properties}}
            cell_export.update(cell_data)
        return cell_export

    def export_json_str(self, export_dict):
        """Exports dict of Cell structure to json string.
        export_dict: Dictionary of Cell structure, generated by <Engine>.export_cells()"""

        return dumps(export_dict, indent = 4)

    def extend_properties(self, calcs):
        """Extends finalized cell properties with values from External Property Calculators.
        calcs: list of External Property Calculators. E.g. the same as passed to <Engine>.apply_rules()"""

        for cell in self._cells_final:
            for calculator in calcs:
                if calculator:
                    resources = calculator.get_resources_cell()
                    cell_properties = {r: cell.properties(r) for r in resources}
                    calc_property = calculator.calc(cell_properties)
                    cell.add_ext_property(calc_property)

    def test(self):
        for cell in self._cells_final:
            bottom_top_f = cell.faces(0, 5)
            print('cell: ', cell)
            for face in bottom_top_f:
                vert_locs = face.get_vertex_locations()
                print('FACE: ', face, ' VERTS: ', vert_locs)
            print('\n')
