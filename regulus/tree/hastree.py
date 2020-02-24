from traitlets import directional_link, HasTraits, TraitError, observe, validate, Int, Instance
from .tree import Tree
from .traittypes import TreeType


class HasTree(HasTraits):
    tree = TreeType(allow_none=True)

    def __init__(self, tree=None):
        self._link = None
        super().__init__()
        if tree is not None:
            self.tree = tree

    @validate('tree')
    def validate_tree(self, proposal):
        print('>> HasTree validate tree', proposal)
        src = proposal['value']

        if src == self.tree:
            return

        link = None

        if isinstance(src, Tree):
            tree = src
        elif isinstance(src, HasTraits) and src.has_trait('tree'):
            tree = getattr(src, 'tree')
            link = directional_link((src, 'tree'), (self, 'tree'))
        elif hasattr(src, 'tree'):
            tree = getattr(src, 'tree')
        elif src is None:
            tree = None
        else:
            raise TraitError('must be a tree or an owner of a tree')

        if self._link is not None:
            self._link.unlink()
        self._link = link
        print('<< HasTree validate tree')
        return tree

    # @observe('tree')
    # def act(self, change):
    #     print(f'HasTree received a new tree {change["new"]}')
