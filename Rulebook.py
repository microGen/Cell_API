'''
Rulebook, contains all the functions to govern over cell splitting.

Implemented properties:
+core properties:
-- all:                 <cell>.coreProperties()
--- location:           <cell>.location()
--- dimensions:         <cell>.dimensions()
--- volume:             <cell>.volume()
+external properties:
-- all:                 <cell>.extProperties()
--- density:            <cell>.density()
--- Young's modulus:    <cell>.youngs()
--- Poisson's ratio:    <cell>.poisson()

example:
def rule_density(grid_data, cell_density)
    return grid_data['density'] > cell_density
'''