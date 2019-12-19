import pandas as pd
from regulus.tree import HasTree, Node, Tree
from regulus.core import HasAttrs


class Partition(object):
    def __init__(self, id_, persistence, pts_span=None, minmax_idx=None, extrema=(), max_merge=False,
                 base=None, regulus=None):
        self.id = id_
        self.regulus = regulus
        self.persistence = persistence

        self.pts_span = pts_span if pts_span is not None else [0, 0]
        self.minmax_idx = minmax_idx if minmax_idx is not None else []
        self.extrema = list(extrema)
        self.max_merge = max_merge
        self.base = base

        self._idx = None
        self._x = None
        self._original_x = None
        self._y = None
        self._values = None

    def __str__(self):
        return f'Partition<{self.id}: persistence:{self.persistence} span:{self.pts_span} extrema:{self.extrema}'

    def _get_pts(self):
        idx = self.idx
        self._x = self.regulus.pts.x.loc[idx]
        self._y = self.regulus.y[idx]

    def internal_size(self):
        return self.pts_span[1] - self.pts_span[0]

    def size(self):
        return len(self.idx)

    @property
    def idx(self):
        if self._idx is None:
            loc = self.regulus.pts_loc
            # idx = loc[self.pts_span[0]:self.pts_span[1] - 1]
            idx = loc[self.pts_span[0]:self.pts_span[1]]
            # idx = [loc[i] for i in range(self.pts_span[0], self.pts_span[1] - 1)]
            idx.extend(self.extrema)
            self._idx = idx
        return self._idx

    @property
    def x(self):
        if self._x is None:
            idx = self.idx
            self._x = self.regulus.pts.x.loc[idx]
        return self._x

    @property
    def original_x(self):
        if self._original_x is None:
            idx = self.idx
            self._original_x = self.regulus.pts.original_x.loc[idx]
        return self._original_x

    @property
    def y(self):
        if self._y is None:
            idx = self.idx
            self._y = self.regulus.y[idx]
        return self._y

    @property
    def values(self):
        if self._values is None:
            if self._idx is None:
                self._get_pts()
            self._values = self.regulus.pts.values.loc[self._idx]
        return self._values

    def max(self):
        return self.regulus.y[self.minmax_idx[1]]

    def min(self):
        return self.regulus.y[self.minmax_idx[0]]

    def gc(self):
        self._x = None
        self._y = None


class RegulusTree(Tree, HasAttrs):
    def __init__(self, regulus, root=None, auto=None):
        Tree.__init__(self, root)
        HasAttrs.__init__(self, regulus.attr, auto or [])
        self.regulus = regulus
        self._persistence_levels = None
        self._partitions = {}
        self.root = root

    def clone(self, root=None):
        return RegulusTree(root=root, regulus=self.regulus, auto=self.auto)

    @property
    def root(self):
        return super().root

    @root.setter
    def root(self, value):
        if isinstance(value, list):
            if len(value) == 1:
                value = value[0]
            else:
                value = Node(ref=-1, data=Partition(-1, 1, pts_span=[0, self.regulus.pts.size()], regulus=self.regulus),
                             children=value, offset=0)
        self._root = value
        self.attr['data_size'] = self.regulus.pts.size()
        if value is not None and value.parent is None:
            sentinal = Node(ref=-1, data=Partition(-1, 1, regulus=self.regulus),
                            children=[value], offset=0)
        for p in self.partitions():
            self._partitions[p.id] = p

        for node in self:
            if not hasattr(node, 'offset'):
                node.offset = 0
            if not hasattr(node, 'regulus'):
                node.regulus = self.regulus

    def retrieve(self, name):
        attr = self.attr[name]
        for node in self:
            attr.compute(node)  # ensure data is computed
        return attr.cache

    def iter_attr(self, attr):
        values = self.attr[attr]
        for node in self:
            yield values[node]

    def partitions(self):
        return self.items()

    def partitions_with_parent(self):
        for node in iter(self):
            yield node.data, node.parent.data

    def at_persistence(self, level):
        partitions = set()
        for p, parent in self.partitions_with_parent():
            if p.persistence <= level < parent.persistence:
                partitions.add(p)
        return partitions

    def partition(self, id):
        return self._partitions.get(id, None)

    def find_partitions(self, selector):
        if isinstance(selector, int):
            f = lambda p: p.id == selector
        elif callable(selector):
            f = selector
        else:
            f = lambda p: p.id in selector
        return list(filter(f, self.partitions()))

    def persistence_levels(self):
        if self._persistence_levels is None:
            levels = {p.persistence for p in self.partitions()}
            self._persistence_levels = sorted(levels)
        return self._persistence_levels


class Regulus(HasAttrs, HasTree):
    def __init__(self, pts, pts_loc, measure, tree=None, type='smale'):
        super().__init__()
        self.type = type
        self.filename = None
        self.pts = pts
        self.pts_loc = pts_loc
        self.measure = measure
        self.y = pts.y(measure)
        self.tree = tree if tree is not None else RegulusTree(regulus=self)

    @property
    def scaler(self):
        return self.pts.scaler

    @property
    def x(self):
        return self.pts.x

    @property
    def values(self):
        return self.pts.values

    @property
    def pts_with_values(self):
        return pd.merge(left=self.pts.x,
                        right=self.pts.values,
                        left_index=True,
                        right_index=True)

    @property
    def pts_with_y(self):
        return pd.merge(left=self.pts.x,
                        right=self.y,
                        left_index=True,
                        right_index=True)

    def apply(self, f):
        for node in self.tree:
            f(node.data, node=node)

    def partitions(self):
        return self.tree.partitions()

    def find_partitions(self, selector):
        return self.tree.find_partions(selector)

    def partition(self, id):
        return self.tree.partition(id)

    def nodes(self):
        return iter(self.tree)

    def find_nodes(self, ids):
        s = set(ids)
        nodes = []
        for node in self.nodes():
            if node.id in s:
                nodes.append(node)
                s.remove(node.id)
                if len(s) == 0:
                    break
        return nodes

    def gc(self):
        for p in self.tree.partitions():
            p.gc()

