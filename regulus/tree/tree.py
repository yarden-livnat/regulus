from uuid import UUID
from .traverse import traverse


class Node(object):
    def __init__(self, data=None, parent=None, children=None, **kwargs):
        self.data = data
        self.parent = parent
        self._children = []
        for key in kwargs:
            setattr(self, key, kwargs[key])

        if children:
            for child in children:
                self.add_child(child)
        if parent:
            parent.add_child(self)

    # def __str__(self):
    #     if 'id' in self.data:
    #         return str(self.data['id'])
    #     else:
    #         return "<none>"

    def __iter__(self):
        return traverse(self)

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
        parent = self.parent
        while parent:
            yield parent
            parent = parent.parent

    def leaves(self, is_leaf=lambda n:n.is_leaf()):
        for node in depth_first(self, is_leaf):
            if is_leaf(node):
                yield node

    def items(self, **kwargs):
        for node in traverse(self, **kwargs):
            if node.data is not None:
                yield node.data

    def depth(self):
        _depth = 0
        for node, d in traverse(self, depth=True):
            if d > _depth:
                _depth = d
        return _depth

    def size(self):
        n = 0
        for node in traverse(self):
            n += 1
        return n



class Tree(object):
    def __init__(self, root=None, name=None):
        self.root = root
        self.name = name if not None else UUID()
