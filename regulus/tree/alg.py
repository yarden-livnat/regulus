from copy import copy
from .tree import Node


def noop(x):
    return x


def with_parent(iterator):
    for node in iterator:
        yield [node.data, node.parent.data if node.parent is not None else None]
