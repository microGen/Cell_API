import Factories

debug_cell = False
debug_json = True

print('Hello World, this is the testing stage for the cell structure as of now')

loc = [1, 1, 1]
dim = [2, 2, 2]

c = Factories.cellFactory(3, loc, dim, {}, False)
#cont = Container("json_test_input.txt")
#cont = Container()
#cont.loadFile("json_test_input.txt")
cont = Factories.containerFactory("json_test_input.txt")
cont.loadFile("json_test_input.txt")

if debug_cell:
    print('Cell data:')
    print('ID:\t\t\t', c.ID())
    print('Pos:\t\t', c.location())
    print('Dims:\t\t', c.dimensions())
    print('MinMax:\t\t', c.minmax())
    print('Volume:\t\t', c.volume())
    print('CoreProps:\t', c.coreProperties())
    print('ExtProps:\t', c.extProperties())
    print(c.vertices(), '\n')
    print(c.vertices(1), '\n')
    print(c.vertices([0, 2, 3]), '\n')
    print(c.edges(), '\n')
    print(c.faces(), '\n')

if debug_json:
    print('Input Data:')
    print(cont.dumpData())
    print(cont.getNearestData([-432432, -42343242, 4234324]))
    print(cont.getEnclosedData([[4, 5], [4, 5], [4, 5]]))
    print(cont.getData([[4, 5], [4, 5], [4, 5]]))
    print('Data fields:\t\t', cont.lengthOfData())

# class test1:
#     def __init__(self, indata):
#         self.__indata = indata
#
#     def murks(self):
#         for i in range(len(self.__indata)):
#             self.__indata[i] + 1
#
#     def hurks(self, indata2):
#         for i in range(len(indata2)):
#             indata2[i]+1
#
# a = [1, 2, 3]
# t = test1(a)
# t.murks()
# print(a)
# t.hurks(a)
# print(a)