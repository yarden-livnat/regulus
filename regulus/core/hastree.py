from traitlets import Bool, HasTraits, Instance, Set, This
from regulus.tree import Tree


class HasTree(HasTraits):
    _tree = Instance(klass=Tree, allow_none=True)
    _owner = This(allow_none=True)

    def __init__(self, tree=None, **kwargs):
        super().__init__(**kwargs)
        self.tree = tree

    @property
    def tree(self):
        return self._tree

    @tree.setter
    def tree(self, src):
        self.set(src)

    @property
    def owner(self):
        return self._owner

    def set(self, src):
        if self._owner is not None:
            self._owner.unobserve(self.ref_tree_changed, names='_tree')
        self.update(src)

    def ref_tree_changed(self, change):
        self.update(self._owner)

    def update(self, src):
        if isinstance(src, Tree):
            self._owner = None
            self._tree = src
        elif isinstance(src, HasTree):
            self._owner = src
            self._tree = src.tree
            self._owner.observe(self.ref_tree_changed, names='_tree')