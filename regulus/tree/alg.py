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

    root = None
    if tree.root is not None:
        root = _reduce(tree.root, 0)
        # if len(roots) == 1:
        #     root = roots[0]
        # else:
        #     root = roots
        # create a fake root
        # if tree.root.parent is not None:
        #     sentinal = copy(tree.parent)
        #     sentinal.add_child(root)

    return tree.clone(root=root)


def with_parent(iterator):
    for node in iterator:
        yield [node.data, node.parent.data if node.parent is not None else None]
