from .tree import Node


def reduce(root, func, factory=Node):
    def _reduce(node):
        children = []
        for child in node.children:
            children.extend(_reduce(child))
        if func(node):
            return [factory(data=node.data, children=children)]
        else:
            return children

    roots = _reduce(root)
    if len(roots) == 1:
        return roots[0]
    return factory(children=roots)
