
from regulus.tree import Tree, Node
from .hasattrs import HasAttrs


class Regulus(HasAttrs):
    def __init__(self, pts, pts_loc, measure, tree=None, type='smale', auto=[]):
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

    def nodes(self):
        return iter(self.tree)

    def gc(self):
        for p in self.partitions():
            p.gc()


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
                value = Node(ref=-1, data=Partition(-1, 1, pts_span=[0, self.regulus.pts.size()],regulus=self.regulus),
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
            attr[node]  # ensure data is computed
        return attr.cache


class Partition(object):
    def __init__(self, id_, persistence, pts_span=None, minmax_idx=None, max_merge=False, regulus=None):
        self.id = id_
        self.regulus = regulus
        self.persistence = persistence

        self.pts_span = pts_span if pts_span is not None else [0, 0]
        self.minmax_idx = minmax_idx if minmax_idx is not None else []
        self.max_merge = max_merge

        self._x = None
        self._y = None

    def __str__(self):
        return str(self.id)

    def size(self):
        return self.pts_span[1] - self.pts_span[0]

    def _get_pts(self):
        loc = self.regulus.pts_loc
        idx = [loc[i] for i in range(self.pts_span[0], self.pts_span[1]-1)]
        idx.extend(self.minmax_idx)
        self._x = self.regulus.pts.x.loc[idx]
        self._y = self.regulus.y[idx]

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

    def max(self):
        return self.regulus.y[self.minmax_idx[1]]

    def min(self):
        return self.regulus.y[self.minmax_idx[0]]

    def gc(self):
        self._x = None
        self._y = None
