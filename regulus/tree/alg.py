from .tree import Node


def noop(x):
    return x


def reduce(root, filter=noop, select=noop, factory=Node):

    def _reduce(node):
        children = []
        for child in node.children:
            children.extend(_reduce(child))
        if filter(node):
            return [factory(data=select(node.data), children=children)]
        else:
            return children

    roots = _reduce(root)
    if len(roots) == 1:
        return roots[0]
    # create a fake root
    return factory(children=roots)


def with_parent(iterator):
    for node in iterator:
        yield [node.data, node.parent.data if node.parent is not None else None]
