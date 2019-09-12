from traitlets import HasTraits
from .adaptive_tree import AdaptiveTree


class SimplifiedTree(AdaptiveTree):
    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, f):
        if self._filter is not None and isinstance(self._filter, HasTraits):
            self.filter.unobserve(self._apply, names='changed')
        self._filter = f
        if self._filter is not None and isinstance(self._filter, HasTraits):
            self._filter.observe(self._apply, names='changed')

    def __init__(self, src, f):
        super().__init__(None, self._reduce)
        self._filter = None
        self.filter = f
        self.src = src

    def _reduce(self, src):
        if self._filter is not None:
            return src.reduce(self._filter)
        return src
