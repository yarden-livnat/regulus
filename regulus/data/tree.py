from collections import deque
from heapq import heappush, heappop


class Node(object):
    def __init__(self, data=None, parent=None, children=None):
        self.data = data
        self.parent = parent
        self._children = list(children) if children is not None else []
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
        for node in depth_first(self,is_leaf):
            if is_leaf(node):
                yield node


class Tree(object):
    def __init__(self, root=None):
        self.root = root


class Visited(object):
    def __init__(self, node):
        self.visited = node


def breath_first(root, is_leaf=lambda n: n.is_leaf(), pre=True, post=False):
    queue = deque()
    queue.append(root)
    while queue:
        node = queue.popleft()
        if isinstance(node, Visited):
            yield node.visited
        else:
            if pre:
                yield node
            if not is_leaf(node):
                queue.extend(node.children)
            if post:
                queue.append(Visited(node))


def depth_first(root, is_leaf=lambda n: n.is_leaf(), pre=True, post=False):
    queue = deque()
    queue.append(root)
    while queue:
        node = queue.pop()
        if isinstance(node, Visited):
            yield node.visited
        else:
            if pre:
                yield node
            if post:
                queue.append(Visited(node))
            if not is_leaf(node):
                queue.extend(reversed(node.children))


def best_first(root, value, is_leaf:lambda n: n.is_leaf()):
    heap = []
    for node in depth_first(root, is_leaf):
        heappush(heap, [value(node), node])
    while heap:
        item = heappop(heap)
        yield item


def traverse(root, direction='depth', is_leaf=lambda n: n.is_leaf(), pre=True, post=False):
    if direction not in ['depth', 'breath']:
        raise Exception('direction must be one of [depth, breath]')
    if direction == 'depth':
        yield depth_first(root, is_leaf, pre, post)

