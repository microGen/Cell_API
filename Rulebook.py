"""
Rulebook, contains functionality to govern over cell splitting.
Define classes in order to implement new features.
Custom rules inherit from class Rule in order to implement common functionality like returning of property name.
Works in conjuction with ExtPropCalc.py, which calculates properties that are external to the core cell data,
e.g. density.

Implemented properties:
+core properties:
--- location:           <cell>.properties('location')
--- dimensions:         <cell>.properties('dimension')
--- volume:             <cell>.properties('volume')
+external properties:
--- material density:   <cell>.properties('mat_density')
--- Young's modulus:    <cell>.properties('youngs')
--- Poisson's ratio:    <cell>.properties('poisson')
--- cell density:       ExtPropCalc.CellDensity
"""

from ExtPropCalc import CellDensity

class Rule:
    """Prototype Rule"""

    grid_resources = None
    cell_resources = None
    gradient_orientation = None

    def __init__(self):
        pass

    @classmethod
    def get_prop(cls):
        """Name of the property that a child class generates."""
        return(cls.prop)

    @classmethod
    def get_resources_grid(cls):
        """Name(s) of the grid resources (properties) that a child class needs to generate results"""
        return cls.grid_resources

    @classmethod
    def get_resources_cell(cls):
        """Name(s) of the cell resources (properties) that a child class needs to generate results"""
        return cls.cell_resources

    @classmethod
    def get_orientation(cls):
        """Returns whether splitting the cell is done orthogonal or parallel to a property gradient for given rule"""
        return cls.gradient_orientation


class Density_min(Rule):
    """Tests cell against set density: Cell density target is lower than given grid point density"""

    grid_resources = ('density',)
    cell_resources = CellDensity.get_resources_cell()
    gradient_orientation = ('orthogonal',)

    def __init__(self):
        pass

    @classmethod
    def apply(cls, grid_data, cell_data):
        """Returns true if cell density is lower than set density"""
        cell_data_calc = CellDensity.calc(cell_data)
        return grid_data['density'] >= cell_data_calc['density']


class Density_max(Rule):
    """Tests cell against set density: Cell density target is higher than given grid point density"""

    grid_resources = ('density',)
    cell_resources = CellDensity.get_resources_cell()
    gradient_orientation = ('orthogonal',)

    def __init__(self):
        pass

    @classmethod
    def apply(cls, grid_data, cell_data):
        """Returns true if cell density is higher than set density"""
        cell_data_calc = CellDensity.calc(cell_data)
        return grid_data['density'] <= cell_data_calc['density']


class Shell_Dist(Rule):
    """Compares allowed minimum distance threshold stored in cell with actual distance from shell"""

    grid_resources = ('shell_dist',)
    cell_resources = ('threshold_dist',)
    gradient_orientation = ('orthogonal',)

    def __init__(self):
        pass

    @classmethod
    def apply(cls, grid_data, cell_data):
        """Returns true if cell distance to shell is smaller than threshold"""
        return grid_data['shell_dist'] < cell_data['threshold_dist']