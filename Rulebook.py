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

    # def getProp(self):
    #     """Returns name of the property that the rule uses"""
    #     return self.__prop_name
    #
    # def getResources(self):
    #     """Returns list of necessary resources to implement calculator or rule"""
    #     return self.__resources

    @classmethod
    def getProp(cls):
        return(cls.prop)

    @classmethod
    def getResources(cls):
        return cls.resources


########################################################################################################################
########################################################################################################################



class Density_min(PropRule):
    """Tests cell against set density."""

    prop = 'mat_density'

    def __init__(self):
        pass

    @classmethod
    def apply(cls, grid_data, cell_density):
        """Returns true if cell density is lower than set density"""
        return grid_data[cls.getProp()] > cell_density


class Density_min(PropRule):
    """Tests cell against set density."""

    prop = 'mat_density'

    def __init__(self):
        pass

    @classmethod
    def apply(cls, grid_data, cell_density):
        """Returns true if cell density is higher than set density"""
        return grid_data[cls.getProp()] < cell_density