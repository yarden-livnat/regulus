from traitlets import HasTraits, Instance, TraitError,directional_link, observe, validate
from regulus.core.traittypes import Function
from regulus.core.mutable import Mutable
from .tree import Tree
from .traittypes import TreeType
from .hastree import HasTree


class TransformTree(HasTree):
    # tree = Instance(klass=Tree, allow_none=True)
    src = TreeType(allow_none=True)
    op = Function(None, allow_none=True)

    def __init__(self, src=None, op=None):
        super().__init__()
        self._link = None
        if src is not None:
            self.src = src
        if op is not None:
            self.op = op

    @validate('src')
    def _src(self, proposal):
        value = proposal['value']
        # print(f'{self.id}: validate src = {value}')
        link = None

        if isinstance(value, Tree):
            src = value
        elif isinstance(value, HasTraits) and value.has_trait('tree'):
            src = getattr(value, 'tree')
            link = directional_link((value, 'tree'), (self, 'src'))
        elif hasattr(value, 'tree'):
            src = getattr(value, 'tree')
        elif value is None:
            src = None
        else:
            raise TraitError('must be a tree or an owner of a tree')

        if self._link is not None:
            self._link.unlink()
        self.link = link
        return src

    @observe('op')
    def _op(self, change):
        old = change['old']
        if isinstance(old, Mutable):
            old.unobserve(self._apply, names='version')

        new = change['new']
        if isinstance(new, Mutable):
            new.observe(self._apply, names='version')

        self._apply()

    @observe('src')
    def _apply(self, change=None):
        if self.src is not None and self.op is not None:
            self.tree = self.op(self.src)
        elif self.tree is not None:
            self.tree = None

