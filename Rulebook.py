"""
Rulebook, contains functionality to govern over cell splitting.
Define classes in order to implement new features.
Custom rules inherit from class Rule in order to implement common functionality like returning of property name.
Works in conjuction with ExtPropCalc.py, which calculates properties that are external to the core cell data,
e.g. density.

Implemented properties:
+core properties:
-- all:                 <cell>.coreProperties()
--- location:           <cell>.location()
--- dimensions:         <cell>.dimensions()
--- volume:             <cell>.volume()
+external properties:
-- all:                 <cell>.extProperties()
--- material density:   <cell>.extProperties('density')
--- Young's modulus:    <cell>.extProperties('youngs')
--- Poisson's ratio:    <cell>.extProperties('poisson')
--- cell density:       ExtPropCalc.cellDensity()
"""

class PropRule:
    """Prototype Property Calculator / Rule"""

    def __init__(self, prop_name, *ressources):
        self.__prop_name = prop_name
        self.__ressources = ressources

    def getProp(self):
        """Returns name of the property that the rule uses"""
        return self.__prop_name

    def getResources(self):
        """Returns list of necessary resources to implement calculator or rule"""
        return self.__ressources



########################################################################################################################
########################################################################################################################



class Density_min(PropRule):
    """Tests cell against set density."""

    def __init__(self):
        super().__init__('mat_density')

    def apply(self, grid_data, cell_density):
        """Returns true if cell density is lower than set density"""
        return grid_data[self.getProp()] > cell_density


class Density_min(PropRule):
    """Tests cell against set density."""

    def __init__(self):
        super().__init__('mat_density')

    def apply(self, grid_data, cell_density):
        """Returns true if cell density is higher than set density"""
        return grid_data[self.getProp()] < cell_density