"""Cell Framework
Copyright (c) 2019 N.Wichmann

Licensed under the Mozilla Public License 2.0
(see attached License.txt or https://www.mozilla.org/en-US/MPL/2.0/)

Factory functions"""

from Cell import Cell
from Container import Container
from Engine import Engine

def cell(serial_number, location, dimensions, ext_properties):
    """Decides between returning a prototype cell or a final cell"""
    cell_instance = Cell(serial_number, location, dimensions, ext_properties)
    return cell_instance

def container(*args):
    """Returns a container object."""

    if args == ():
        container_instance = Container()
    else:
        container_instance = Container(args[0])
    return container_instance

def engine(*args):
    """Returns an arbiter object."""

    if args == ():
        arbiter_instance = Engine()
    elif len(args) == 1:
        arbiter_instance = Engine(args[0])
    else:
        arbiter_instance = Engine(args)
    return arbiter_instance