
class HierarchicalComplex(object):
    def __init__(self, pts, root=None):
        self.filename = None
        self.pts = pts
        self.root = root

    def apply(self, f):
        for node in self.root:
            f(node.data, node=node)


class Partition(object):
    def __init__(self, id_, persistence, span=None, minmax_idx=None, max_merge=False, topology=None):
        self.id = id_
        self.topology = topology
        self.persistence = persistence

        self.span = span if span is not None else []
        self.minmax_idx = minmax_idx if minmax_idx is not None else []
        self.max_merge = max_merge

        self._x = None
        self._y = None
        self._models = dict()
        self.attr = dict()

    def __str__(self):
        return str(self.id)

    @property
    def models(self):
        return self._models

    def _get_pts(self):
        idx = [*range(*self.span)]
        idx.extend(self.minmax_idx)
        self._x = self.topology.pts.x.loc[idx]
        self._y = self.topology.pts.y[idx]

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
