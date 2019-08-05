from Cell import Cell, CellFinal
from Container import Container
from Arbiter import Arbiter

def CELL(serial_number, location, dimensions, ext_properties, state):
    """Decides between returning a prototype cell or a final cell"""

    if not state:
        cell_instance = Cell(serial_number, location, dimensions, ext_properties)
    else:
        cell_instance = CellFinal(serial_number, location, dimensions, ext_properties)

    return cell_instance

########################################################################################################################


def CONTAINER(*args):
    """Returns a container object."""

    if args == ():
        container_instance = Container()
    else:
        container_instance = Container(args[0])

    return container_instance

########################################################################################################################


def ARBITER(*args):
    """Returns an arbiter object."""

    if args == ():
        arbiter_instance = Arbiter()
    elif len(args) == 1:
        arbiter_instance = Arbiter(args[0])
    else:
        arbiter_instance = Arbiter(args)

    return arbiter_instance