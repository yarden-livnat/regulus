from collections import defaultdict
from traitlets import HasTraits, Tuple, Unicode
from .cache import Cache


def minmax(obj):
    min = max = None
    for item in iter(obj):
        if item is not None:
            if min is None:
                min = max = item
            elif item < min:
                min = item
            elif item > max:
                max = item
    return min, max


class AttrRange(object):
    def __init__(self, type='fixed', v=(0,1)):
        self.value = v
        self._constrain = v
        self._type = type

    def update(self, tree, attr):
        if self._type != 'fixed':
            r = minmax(tree.iter_attr(attr))
            if self._type == 'auto':
                self.value = r
            elif self._type == 'constrained':
                self.value = max(self._constrain[0], r[0]), min(self._constrain[1], r[1])
        return self.value


def _attr_key(obj):
    if isinstance(obj,tuple):
        return ':'.join(map(lambda o: str(o.id), obj))
    if hasattr(obj, 'id'):
        return obj.id
    return obj


def _dict(_):
    return dict()


def _wrap_factory(context, func):
    def wrapper(a):
        if isinstance(a, tuple):
            return func(context, *a)
        return func(context, a)
    return wrapper


class HasAttrCache(Cache):
    def __init__(self, parent):
        super().__init__(parent)
        self.context = self

    def __getitem__(self, obj):
        # print(f'HasAttrCache: id: {id(self)}  context: {id(self.context)}' )
        key = _attr_key(obj)
        value = None
        if key in self.cache:
            return self.cache[key]

        if self.parent:
            value, found = self.parent.get(key)
            if found:
                if isinstance(value, Cache) and value.dynamic:
                    value = Cache(key=value.key, factory=value.factory, dynamic=True,
                                  context=self.context, save=value.save, **value.properties)
                    self.cache[key] = value
                return value
        self.cache[key] = dict()
        return self.cache[key]


class HasAttrs(HasTraits):

    state = Tuple(Unicode(), Unicode())

    def __init__(self, parent=None, auto=()):
        super().__init__()
        # print('HasAttrs', id(self))
        self.parent = parent
        range = None
        if parent is not None:
            range=parent.properties.get('range', None)

        # self.attr = Cache(parent, factory=None, range=range, context=None)
        self.attr = HasAttrCache(parent)
        self.auto = []
        self.dependencies = defaultdict(list)
        for entry in auto:
            self.add_attr(*entry)

    def add_attr(self, factory, name=None, dynamic=False, key=_attr_key, range=None, requires=(), save=True, **kwargs):
        """override previous attribute if one exists"""
        if name is None:
            if factory.__name__ == '<lambda>':
                print('Error: a name must be given for a lambda expression')
                return
            name = factory.__name__

        for d in requires:
            self.dependencies[d].append(name)

        if range is None:
            range = AttrRange('auto')

        if name not in self.attr:
            op = 'add'
        else:
            op = 'change'
        self.attr[name] = Cache(key=key, factory=factory, dynamic=dynamic, context=self.attr, range=range, save=save, **kwargs)
        self.state = (op, name)

        self.reset_dependents(name)
        # for i, entry in enumerate(self.auto):
        #     if entry[1] == name:
        #         self.auto[i] = [factory, name, key, range]
        #         break
        # else:
        #     self.auto.append([factory, name, key, range])

    def update_attr(self, factory, name=None):
        if name is None:
            if factory.__name__ == '<lambda>':
                print('Error: a name must be given for a lambda expression')
                return
            name = factory.__name__
        if name in self.attr:
            self.attr[name].factory = factory
            self.state = ('change', name)
            self.reset_dependents(name)
        else:
            raise ValueError(f'Attribute {name} not found')

    def clear_attr(self, name):
        if name in self.attr:
            self.attr[name].clear()
            self.state = ('change', name)
        else:
            raise ValueError(f'Attribute {name} not found')

    def reset_dependents(self, name):
        for d in self.dependencies[name]:
            self.clear_attr(d)

    def alias(self, new, old):
        if old in self.attr:
            self.attr[new] = self.attr[old]
            self.reset_dependents(new)
        else:
            raise ValueError(f'Attribute {old} not found')

    def __contains__(self, attr):
        """check is attr in cache"""
        return attr in self.attr

    def __setstate__(self, state):
        self.__dict__.update(state)
        # for factory, name, key, range in self.auto:
        #     # self.attr[name].factory = factory
        #     self.attr[name].factory = _wrap_factory(self.attr, factory)


UNIT_RANGE = AttrRange(type='fixed', v=(0,1))