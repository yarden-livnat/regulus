from regulus.topo.cache import Cache


def minmax(obj):
    items = iter(obj)
    min = max = next(items)
    for item in items:
        if item < min:
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
    return obj.id


def _dict(_):
    return dict()


def _wrap_factory(context, func):
    def wrapper(a):
        if isinstance(a, tuple):
            return func(context, *a)
        return func(context, a)
    return wrapper


class HasAttrs(object):
    def __init__(self, parent=None, auto=()):
        self.attr = Cache(parent, factory=_dict)
        self.auto = []
        for entry in auto:
            self.add_attr(*entry)

    def add_attr(self, factory, name=None, key=_attr_key, range=None, **kwargs):
        if name is None:
            if factory.__name__ == '<lambda>':
                print('Error: a name must be given for a lambda expression')
                return
            name = factory.__name__

        if range is None:
            range = AttrRange('auto')

        self.attr[name] = Cache(key=key, factory=_wrap_factory(self.attr, factory), range=range, **kwargs)
        for i, entry in enumerate(self.auto):
            if entry[0] == name:
                self.auto[i] = [name, factory, key]
                break
        else:
            self.auto.append([name, factory, key])

    def __contains__(self, attr):
        """check is attr in cache"""
        return attr in self.attr

    def __setstate__(self, state):
        self.__dict__.update(state)
        for name, factory, key in self.auto:
            self.attr[name].factory = _wrap_factory(self.attr, factory)


UNIT_RANGE = AttrRange(type='fixed', v=(0,1))