from regulus.utils.cache import Cache

def _attr_key(obj):
    if isinstance(obj,tuple):
        return ':'.join(map(lambda o: str(o.ref), obj))
    return obj.ref

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

    def add_attr(self, name, factory, key=_attr_key):
        self.attr[name] = Cache(key=key, factory=_wrap_factory(self.attr, factory))
        self.auto.append([name, factory, key])

    def __contains__(self, attr):
        """check is attr in cache"""
        return attr in self.attr

    def local(self):
        return self.attr.cache
