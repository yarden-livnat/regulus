from traitlets import TraitType
from .tree import Tree


class TreeType(TraitType):
    default_value = None
    info_text = 'a Tree (can accept an object that has a tree)'
    allow_none = True

    def validate(self, obj, value):
        if value is None:
            return value
        if isinstance(value, Tree):
            return value
        if hasattr(value, 'tree'):
            return value
        self.error(obj, value)