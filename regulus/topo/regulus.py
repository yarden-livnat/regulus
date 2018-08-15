
from regulus.utils.cache import Cache
from regulus.tree import Tree, Node

def dict_factory(_):
    return dict()

class RegulusTree(Tree):
    def __init__(self, regulus, root=None):
        super().__init__()
        self.attrs = Cache(parent=regulus.attrs, factory=dict_factory)
        self.regulus = regulus
        self.root = root

    def clone(self, root=None):
        return RegulusTree(root=root, regulus=self.regulus)

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        if isinstance(value, list):
            if len(value) == 1:
                value = value[0]
            else:
                value = Node(ref=-1, data=Partition(-1, 1, regulus=self.regulus),
                             children=value, offset=0)
        self._root = value
        if value is not None and value.parent is None:
            sentinal = Node(ref=-1, data=Partition(-1, 1, regulus=self.regulus),
                            children=[value], offset=0)
        for node in self:
            if not hasattr(node, 'offset'):
                node.offset = 0




class Regulus(object):
    def __init__(self, pts, tree=None):
        self.filename = None
        self.pts = pts
        self.attrs =  Cache(factory=dict_factory)
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


class Partition(object):
    def __init__(self, id_, persistence, span=None, minmax_idx=None, max_merge=False, regulus=None):
        self.id = id_
        self.regulus = regulus
        self.persistence = persistence

        self.span = span if span is not None else [0, 0]
        self.minmax_idx = minmax_idx if minmax_idx is not None else []
        self.max_merge = max_merge

        self._x = None
        self._y = None
        self.models = dict()
        self.measures = dict()

    def __str__(self):
        return str(self.id)


    def size(self):
        return self.span[1] - self.span[0]

    # @property
    # def models(self):
    #     return self._models

    def _get_pts(self):
        idx = [*range(*self.span)]
        idx.extend(self.minmax_idx)
        self._x = self.regulus.pts.x.loc[idx]
        self._y = self.regulus.pts.y[idx]

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

    def gc(self):
        self._x = None
        self._y = None
        self.models = dict()
        self.measures = dict()
