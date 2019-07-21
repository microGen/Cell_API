from Cell import Cell, CellFinal
from Container import Container
from Arbiter import Arbiter

def cellFactory(serial_number, location, dimensions, ext_properties, state):
    """Decides between returning a prototype cell or a final cell"""

    if not state:
        cell_Instance = Cell(serial_number, location, dimensions, ext_properties)
    else:
        cell_Instance = CellFinal(serial_number, location, dimensions, ext_properties)

    return cell_Instance

def containerFactory(*args):
    """Returns a container object."""

    if args == ():
        container_instance = Container()
    else:
        container_instance = Container(args[0])

    return container_instance

def arbiterFactory(*args):
    """Returns an arbiter object."""

    if args == ():
        arbiter_instance = Arbiter()
    else:
        arbiter_instance = Arbiter(args)

    return arbiter_instance