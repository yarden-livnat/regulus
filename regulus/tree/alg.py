from copy import copy
from .tree import Node


def noop(x):
    return x


def with_parent(iterator):
    for node in iterator:
        yield [node.data, node.parent.data if node.parent is not None else None]


def reduce_tree(tree, filter=noop, select=noop, factory=Node):

    def _reduce(node, offset, depth):
        # print('.'*depth, node.ref,' #children:',len(node.children))
        children = []
        child_offset = offset
        for child in node.children:
            children.extend(_reduce(child, child_offset, depth+1))
            child_offset += child.data.size()
        if filter(tree, node):
            data = select(node.data)
            return [factory(data=data, children=children, offset=offset)]
        else:
            return children

    root = None
    if tree.root is not None:
        root = _reduce(tree.root, 0, 0)
    return tree.clone(root=root)


def filter_tree(tree, func):
    select = set()
    for node in tree:
        if func(tree, node):
             select.add(node.id)
    return select

#
# def tree_filter(tree, func):
#     select = set()
#     for node in tree:
#         if func(tree, node):
#              select.add(node.ref)
#     return select
