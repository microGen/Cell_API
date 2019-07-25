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

class Rule:
    """Prototype Rule"""

    def __init__(self, prop_name):
        self.__prop_name = prop_name

    def getProp(self):
        """Returns name of the property that the rule uses"""
        return self.__prop_name



########################################################################################################################
########################################################################################################################



class Density(Rule):
    """Tests cell against set density."""

    def __init__(self, prop_name):
        super().__init__(prop_name)

    def apply_min(self, grid_data, cell_density):
        """Returns true if cell density is lower than set density"""
        return grid_data[self.getProp()] > cell_density

    def apply_max(self, grid_data, cell_density):
        """Returns true if cell density is higher than set density"""
        return grid_data[self.getProp()] < cell_density