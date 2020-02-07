
from wrapt import ObjectProxy


class DynamicTree(ObjectProxy):
    def __init__(self, src, operator):
        super().__init__(src)
        self._self_attribute = 1

    @property
    def attribute(self):
        return self._self_attribute

    @attribute.setter
    def attribute(self, value):
        self._self_attribute = value

    @attribute.deleter
    def attribute(self):
        del self._self_attribute