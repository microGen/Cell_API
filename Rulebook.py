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
--- material density:   <cell>.properties('density')
--- Young's modulus:    <cell>.properties('youngs')
--- Poisson's ratio:    <cell>.properties('poisson')
--- cell density:       ExtPropCalc.CellDensity
"""

class PropRule:
    """Prototype Property Calculator / Rule"""

    def __init__(self):
        pass

    @classmethod
    def get_prop(cls):
        """Name of the property that a child class generates."""
        return(cls.prop)

    @classmethod
    def get_resources(cls):
        """Name(s) of the resources (properties) that a child class needs to generate results"""
        return cls.resources


########################################################################################################################
########################################################################################################################



class Density_min(PropRule):
    """Tests cell against set density: Cell density target is lower than given grid point density"""

    resources = ('density',)

    def __init__(self):
        pass

    @classmethod
    def apply(cls, grid_data, cell_data):
        """Returns true if cell density is lower than set density"""
        grid_data = grid_data['density']
        cell_data = cell_data['density']
        return grid_data > cell_data


class Density_max(PropRule):
    """Tests cell against set density: Cell density target is higher than given grid point density"""

    resources = ('density',)

    def __init__(self):
        pass

    @classmethod
    def apply(cls, grid_data, cell_data):
        """Returns true if cell density is higher than set density"""
        grid_data = grid_data['density']
        cell_data = cell_data['density']
        return grid_data < cell_data