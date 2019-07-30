from regulus.utils.cache import Cache


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
    def __init__(self, parent=None, auto=[]):
        self.attr = Cache(parent, factory=_dict)
        self.auto = []
        for entry in auto:
            self.add_attr(*entry)

    def add_attr(self, name, factory, key=_attr_key, **kwargs):
        self.attr[name] = Cache(key=key, factory=_wrap_factory(self.attr, factory), **kwargs)
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
