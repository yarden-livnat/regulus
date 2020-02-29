from traitlets import HasTraits, Instance, TraitError,directional_link, observe, validate
from regulus.core.traittypes import Function
from regulus.core.mutable import Mutable
from .tree import Tree
from .traittypes import TreeType


class TransformTree(HasTraits):
    tree = Instance(klass=Tree, allow_none=True)
    src_tree = Instance(klass=Tree, allow_none=True)
    src = TreeType(allow_none=True)
    op = Function(None, allow_none=True)

    def __init__(self, src=None, op=None):
        self._link = None
        super().__init__()
        if src is not None:
            self.src = src
        if op is not None:
            self.op = op

    @validate('src')
    def _src(self, proposal):
        src = proposal['value']
        # print(f'>> TransformTree {id(self)}: validate src = {src}')
        link = None

        if isinstance(src, Tree):
            self.src_tree = src
        elif isinstance(src, HasTraits) and src.has_trait('tree'):
            link = directional_link((src, 'tree'), (self, 'src_tree'))
        elif hasattr(src, 'tree'):
            self.src_tree = getattr(src, 'tree')
        elif src is None:
            self.src_tree = None
        else:
            raise TraitError('must be a tree or an owner of a tree')

        if self._link is not None:
            self._link.unlink()
        self._link = link
        # print(f'<< TransformTree {id(self)}: validate src = {src}')
        return src

    @observe('op')
    def _op(self, change):
        old = change['old']
        if isinstance(old, Mutable):
            old.unobserve(self.apply, names='version')

        new = change['new']
        if isinstance(new, Mutable):
            new.observe(self.apply, names='version')

        self.apply()

    @observe('src_tree')
    def apply(self, _=None):
        # print('>> TransformTree apply')
        if self.src_tree is not None and self.op is not None:
            self.tree = self.op(self.src_tree)
        elif self.tree is not None:
            self.tree = None

