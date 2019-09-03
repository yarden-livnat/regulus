from traitlets import Bool, HasTraits, Instance, Set, This

from regulus.tree import Tree, Node
from regulus.core import HasAttrs, HasTree


class Partition(object):
    def __init__(self, id_, persistence, pts_span=None, minmax_idx=None, max_merge=False, regulus=None):
        self.id = id_
        self.regulus = regulus
        self.persistence = persistence

        self.pts_span = pts_span if pts_span is not None else [0, 0]
        self.minmax_idx = minmax_idx if minmax_idx is not None else []
        self.max_merge = max_merge
        self._idx = None

        self._x = None
        self._y = None
        self._values = None

    def __str__(self):
        return str(self.id)

    def size(self):
        return self.pts_span[1] - self.pts_span[0]

    def _get_pts(self):
        idx = self.idx
        self._x = self.regulus.pts.x.loc[idx]
        self._y = self.regulus.y[idx]
        # self._values =

    @property
    def idx(self):
        if self._idx is None:
            loc = self.regulus.pts_loc
            idx = [loc[i] for i in range(self.pts_span[0], self.pts_span[1] - 1)]
            idx.extend(self.minmax_idx)
            self._idx = idx
        return self._idx

    @property
    def x(self):
        if self._x is None:
            self._get_pts()
        return self._x

    @property
    def y(self):
        if self._y is None:
            self._get_pts()
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
        for node in self:
            if not hasattr(node, 'offset'):
                node.offset = 0

    def retrieve(self, name):
        attr = self.attr[name]
        for node in self:
            attr.compute(node)  # ensure data is computed
        return attr.cache

    def iter_attr(self, attr):
        values = self.attr[attr]
        for node in self:
            yield values[node]


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

    def apply(self, f):
        for node in self.tree:
            f(node.data, node=node)

    def partitions(self):
        return self.tree.items()

    def partition(self, id):
        for p in self.partitions():
            if p.id == id:
                return p
        return None

    def get_partitions(self, l):
        return list(filter(lambda p: p.id in l, self.partitions()))

    def nodes(self):
        return iter(self.tree)

    def gc(self):
        for p in self.partitions():
            p.gc()

