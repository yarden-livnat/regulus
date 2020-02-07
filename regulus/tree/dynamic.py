from traitlets import HasTraits, Int
from wrapt import ObjectProxy


class DynamicTree(ObjectProxy, Volatile):

    def __init__(self, src, op):
        super().__init__(src.clone())
        self._self_src = src
        self._self_op = op
        if isinstance(src, Volatile):
            src.observe(self.invalidate, names='version')

    def _update(self):
        print('DynamicTree.update')
        super()._update()



