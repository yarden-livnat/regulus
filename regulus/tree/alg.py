from copy import copy
from .tree import Node


def noop(x):
    return x


def reduce(tree, filter=noop, select=noop, factory=Node):

    def _reduce(node, offset, depth):
        # print('.'*depth, node.ref,' #children:',len(node.children))
        children = []
        child_offset = offset
        for child in node.children:
            children.extend(_reduce(child, child_offset, depth+1))
            child_offset += child.data.size()
        if filter(node):
            # print(' '*depth, node.ref, 'passed. #children:',len(children))
            data = select(node.data)
            # data['offset'] = offset
            return [factory(data=data, children=children, offset=offset)]
        else:
            # print(' '*depth, node.ref, 'failed. return ',len(children), 'children')
            return children

    root = None
    if tree.root is not None:
        root = _reduce(tree.root, 0, 0)
        # print('reduce: roots:', root)
    return tree.clone(root=root)


def with_parent(iterator):
    for node in iterator:
        yield [node.data, node.parent.data if node.parent is not None else None]
