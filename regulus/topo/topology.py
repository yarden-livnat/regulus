
class Topology(object):
    def __init__(self, pts, partitions=None, tree=None):
        self.filename = None
        self.pts = pts
        self.partitions = partitions
        self.tree = tree


class Partition(object):
    def __init__(self, id_, persistence, span=None, minmax_idx=None, max_merge=False, topo=None):
        self.id = id_
        self.topo = topo
        self.persistence = persistence

        self.span = span if span is not None else []
        self.minmax_idx = minmax_idx if minmax_idx is not None else []
        self.max_merge = max_merge


class Node(object):
    def __init__(self, partition):
        self.partition = partition
        self.parent = None
        self.children = []

    @property
    def id(self):
        return self.partition.id

    def visit(self, visitor):
        def _visit(node):
            visitor(node)
            for child in node.children:
                _visit(child)
        _visit(self)

    def reduce(self, f, value):
        def _reduce(node, acc):
            acc = f(node, acc)
            for child in node.children:
                acc = _reduce(child, acc)
            return acc
        return _reduce(self, value)

    def depth(self):
        def _depth(node, d):
            v = d
            for child in node.children:
                v = max(v, _depth(child, d+1))
            return v
        return _depth(self, 1)

    def size(self):
        return self.reduce(lambda x, v: v+1, 0)