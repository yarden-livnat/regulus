from traitlets import directional_link, HasTraits, TraitError, observe, validate, Int, Instance
from .tree import Tree
from .traittypes import TreeType


class HasTree(HasTraits):
    tree = Instance(klass=Tree, allow_none=True)
    src = TreeType(allow_none=True)

    def __init__(self, src=None):
        self._link = None
        super().__init__()
        if src is not None:
            self.src = src

    @validate('src')
    def validate_src(self, proposal):
        # print(f'>> HasTree {id(self)} validate src\n\t {proposal}')
        src = proposal['value']

        link = None

        if isinstance(src, Tree):
            self.tree = src
        elif isinstance(src, HasTraits) and src.has_trait('tree'):
            link = directional_link((src, 'tree'), (self, 'tree'))
        elif hasattr(src, 'tree'):
            self.tree = getattr(src, 'tree')
        elif src is None:
            self.tree = None
        else:
            raise TraitError('must be a tree or an owner of a tree')

        if self._link is not None:
            self._link.unlink()
        self._link = link
        # print(f'<< HasTree {id(self)} validate src')
        return src

    # @observe('tree')
    # def act(self, change):
    #     print(f'HasTree {id(self)}received a new tree {change["new"]}')
