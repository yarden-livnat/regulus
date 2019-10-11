

def no_op(x):
    return x


class Cache(object):
    _counter = 0

    def __init__(self, parent=None, key=None, factory=None, context=None, save=True, **kwargs):
        self.parent = parent
        self.factory = factory if not None else no_op
        self.context = context
        self.cache = dict()
        self.key = key if key is not None else no_op
        self.properties = kwargs
        self.save = save

    def __getitem__(self, obj):
        key = self.key(obj)
        if key not in self.cache:
            if self.parent:
                value, found = self.parent.get(key)
                if found:
                    return value
            self.cache[key] = self.eval(obj)
        return self.cache[key]

    def __setitem__(self, obj, value):
        key = self.key(obj)
        self.cache[key] = value

    def get(self, key):
        if key in self.cache:
            return [self.cache[key], True]
        if self.parent:
            return self.parent.get(key)
        return [None, False]

    def eval(self, obj):
        if self.factory is None:
            return None
        if isinstance(obj, tuple):
            return self.factory(self.context, *obj)
        return self.factory(self.context, obj)

    def compute(self, obj):
        self.__getitem__(obj)

    def __iter__(self):
        return iter(self.cache)

    def __contains__(self, obj):
        key = self.key(obj)
        return self.has(key)

    def has(self, key):
        return key in self.cache or (self.parent and self.parent.has(key))

    def values(self):
        return dict(self.cache)

    def __getstate__(self):
        """Pickle can't handle the case where the factory can not be found.
        Instead we save the factory metadata. When unpickle is called we try to load the factory ourselves.
        If the factory doesn't exist we don't generate an error. This allows access to existing values though no
        new values can be generated unless the user explicitly set a new factory function
        """
        state = self.__dict__.copy()
        del state['factory']
        state['factory_name'] = self.factory.__name__
        state['factory_module'] = self.factory.__module__
        return state

    def __setstate__(self, state):
        from importlib import import_module
        self.__dict__.update(state)
        try:
            module = import_module(state['factory_module'])
            factory = getattr(module, state['factory_name'])
        except:
            factory = None
        self.factory = factory


