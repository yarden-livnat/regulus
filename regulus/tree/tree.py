from uuid import UUID
from .traverse import traverse, depth_first


class Node(object):
    def __init__(self, id=None, data=None, parent=None, children=None, **kwargs):
        self.id = id if id is not None else data.id if data is not None else -1
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


class Tree(object):
    def __init__(self, root=None):
        self._root = root

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    def clone(self, root=None):
        return Tree(root)

    def leaves(self, is_leaf=lambda n:n.is_leaf()):
        if self.root is None:
            return iter(())
        for node in depth_first(self.root, is_leaf):
            if is_leaf(node):
                yield node

    def items(self, **kwargs):
        if self.root is None:
            return iter(())
        for node in traverse(self.root, **kwargs):
            if node.data is not None:
                yield node.data

    def depth(self):
        _depth = 0
        if self.root is not None:
            for node, d in traverse(self.root, depth=True):
                if d > _depth:
                    _depth = d
        return _depth

    def reduce(self, filter, factory=Node):
        def _reduce(node, offset):
            children = []
            child_offset = offset
            for child in node.children:
                children.extend(_reduce(child, child_offset))
                child_offset += child.data.size()
            if filter(self, node):
                return [factory(data=node.data, children=children, offset=offset)]
            else:
                return children

        root = None
        if self.root is not None:
            root = _reduce(self.root, 0)
        return self.clone(root)

    def prune(self, filter, factory=Node):
        def _prune(node, offset, depth):
            if not filter(self, node):
                return None
            children = []
            child_offset = offset
            for child in node.children:
                c = _prune(child, child_offset, depth+1)
                if c is not None:
                    children.append(c)
                    child_offset += c.data.size()
            return factory(data=node.data, children=children,offset=offset)

        root = None
        if self.root is not None:
            root = _prune(self.root, 0, 0)
        return self.clone(root)

    def filter(self, f):
        select = set()
        for node in self:
            if f(self, node):
                select.add(node.id)
        return select

    def find(self, f):
        for node in self:
            if f(self, node):
                return node
        return None

    def size(self):
        n = 0
        for node in self:
            n += 1
        return n

    def __iter__(self):
        if self._root is None:
            return iter(())
        return traverse(self._root)
