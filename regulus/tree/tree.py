from .algo import depth_first


class Node(object):
    def __init__(self, data=None, parent=None, children=None):
        self.data = data
        self.parent = parent
        self._children = []

        if children:
            for child in children:
                self.add_child(child)
        if parent:
            parent.add_child(self)

    @property
    def children(self):
        return self._children

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return len(self._children) == 0

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def siblings(self):
        if self.parent is not None:
            for child in self.parent.children:
                if child != self:
                    yield child

    def ancestors(self):
        node = self.parent
        while node:
            yield node
            node = node.parent

    def leaves(self, is_leaf=lambda n:n.is_leaf()):
        for node in depth_first(self, is_leaf):
            if is_leaf(node):
                yield node

    def __iter__(self):
        return self.items()

    def items(self):
        for node in depth_first(self):
            if node.data is not None:
                yield node.data



class Tree(object):
    def __init__(self, root=None):
        self.root = root

