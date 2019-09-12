from .hastree import HasTree


class AdaptiveTree(HasTree):
    @property
    def src(self):
        return self._src or self._src_tree

    @src.setter
    def src(self, src):
        if self._src is not None:
            self._src.unobserve(self._apply, names=['change'])

        if isinstance(src, HasTree):
            src.observe(self._apply, names=['change'])
            self._src = src
            self._src_tree = src.tree
        else:
            self._src = None
            self._src_tree = src
        self._apply()

    def __init__(self, src, f):
        super().__init__()
        self.f = f
        self._src = None
        self._src_tree = None
        self.src = src

    def _apply(self, *args):
        if self._src_tree is not None:
            self.set(self.f(self._src_tree))


