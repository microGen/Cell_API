import Factories
import Testing
import Rulebook
from Postprocessor import Postprocessor

print('Testing stage for Cell Framework\n')

Testing.cell_unit_test()
Testing.container_unit_test()
Testing.prop_calc_unit_test()
Testing.rulebook_unit_test()
Testing.helpers_unit_test()

# easy, hacky switch between test cases for framework output
# optimization targets:
# 0: density left: max, right: min
# 1: density top: max, bottom: min
# 2: density gradient top: max, bottom: min
# 3: density left: 50%, distance to shell
testcase = 0

# general settings
iterations = 6
testnames = ['testfile_gen1.json', 'testfile_gen2.json', 'testfile_lim.json', 'testfile_targets.json']
testfiles = ['./testfiles/' + t for t in testnames]
outnames = ['out_gen1.json', 'out_gen2.json', 'out_lim.json', 'out_targtest.json']
outfiles = ['./testfiles/' + o for o in outnames]

# generate optimization settings
rules = [[Rulebook.Density_max],[Rulebook.Density_max],[Rulebook.Density_max],[Rulebook.Density_max, Rulebook.Shell_Dist]]
options = [['min'], ['min'], ['med'], ['min', 'amn']]

# initialize framework
tst_cont = Factories.container(testfiles[testcase])
eng = Factories.engine(tst_cont)

# apply optimization algorithm
eng.create_cell_structure()
eng.evolve_cell_structure(6, rules[testcase], options[testcase], False)

# export cell structure
eng.extend_properties([calc])
export = eng.export_cells('final')
export_string = eng.export_json_str(export)
export_file = open(outfiles[testcase], 'w')
export_file.write(export_string)
export_file.close()

#eng.test()

pp = Postprocessor(eng, 0.1)
#pp.test()