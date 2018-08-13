
class HMSC(object):
    def __init__(self, pts, root=None):
        self.filename = None
        self.pts = pts
        self.tree = root

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
    def __init__(self, id_, persistence, span=None, minmax_idx=None, max_merge=False, hmsc=None):
        self.id = id_
        self.hmsc = hmsc
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
        self._x = self.hmsc.pts.x.loc[idx]
        self._y = self.hmsc.pts.y[idx]

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
