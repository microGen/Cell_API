"""
Rulebook, contains all the functions to govern over cell splitting.
Define functions in order to implement new features.
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

example:
def rule_density(grid_data, cell_density)
    return grid_data['density'] > cell_density
"""

def testrule(grid_data, cell_density):
    return grid_data['density'] > cell_density