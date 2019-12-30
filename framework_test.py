"""Cell Framework
Copyright (c) 2019 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)

TEST PROGRAM FOR ADAPTABLE INFILL STRUCTURE"""

import sys
from time import time, ctime
from datetime import timedelta
import Factories
from unit_tests import Testing
import Rulebook
from ExtPropCalc import CellDensity

print('Testing stage for Cell Framework\n')

Testing.cell_unit_test()
Testing.container_unit_test()
Testing.prop_calc_unit_test()
Testing.rulebook_unit_test()
Testing.helpers_unit_test()

print('\nAll unit tests passed. Proceeding to main program.\n\n')

# easy, hacky switch between test cases for framework output
# optimization targets:
# 0: density left: max, right: min
# 1: density top: max, bottom: min
# 2: density gradient top: max, bottom: min
# 3: density top: 50%, distance to shell bottom
testcase = int(sys.argv[1])
# Iterations of the optimization process. WARNING: 6 iterations will take a few minutes, 12 will likely take hours.
iterations = int(sys.argv[2])

# general settings
testnames = ['testfile_gen1.json', 'testfile_gen2.json', 'testfile_lim.json', 'testfile_targets.json']
testfiles = ['./testfiles/' + t for t in testnames]
outnames = ['out_gen1.json', 'out_gen2.json', 'out_lim.json', 'out_targets.json']
outfiles = ['./testfiles/' + o for o in outnames]

# generate optimization settings
rules = [[Rulebook.Density_max],[Rulebook.Density_max],[Rulebook.Density_max],[Rulebook.Density_max, Rulebook.Shell_Dist]]
options = [['min'], ['min'], ['med'], ['min', 'min']]

time_start = time()
print('Starting Cell Framework:', ctime(time_start), '\n')

# initialize framework
print('Initializing framework...')
tst_cont = Factories.container(testfiles[testcase])
eng = Factories.engine(tst_cont)

# apply optimization algorithm
print('Creating initial cell structure...')
eng.create_cell_structure()
print('Optimizing cell structure (this might take a while)...')
eng.evolve_cell_structure(iterations, rules[testcase], options[testcase], 'high', True)

# export cell structure
#print('Appending further properties to cells...')
#eng.extend_properties([CellDensity])
print('Exporting cell structure...')
export = eng.export_cells('final')
export_string = eng.export_json_str(export)
export_file = open(outfiles[testcase], 'w')
export_file.write(export_string)
export_file.close()
print('Cell structure written to: ', outnames[testcase])
print('\nDONE.')
time_stop = time()
print('\nCell Framework finished: ', ctime(time_stop), ' and took ', str(timedelta(seconds=(time_stop-time_start))))
