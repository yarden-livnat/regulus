from copy import copy
from .tree import Node


def noop(x):
    return x


def reduce(tree, filter=noop, select=noop, factory=Node):

    def _reduce(node, offset):
        children = []
        child_offset = offset
        for child in node.children:
            children.extend(_reduce(child, child_offset))
            child_offset += child.data.size()
        if filter(node):
            data = select(node.data)
            # data['offset'] = offset
            return [factory(data=data, children=children, offset=offset)]
        else:
            return children

    roots = _reduce(tree, 0)
    if len(roots) == 1:
        root = roots[0]
    else:
        root = factory(children=roots)
    # create a fake root
    if tree.parent is not None:
        fake = copy(tree.parent)
        fake.add_child(root)
    return root


def with_parent(iterator):
    for node in iterator:
        yield [node.data, node.parent.data if node.parent is not None else None]
