

def no_op(x):
    return x


class Cache(object):
    def __init__(self, parent=None, key=None, factory=None, **kwargs):
        self.parent = parent
        self.factory = factory if not None else no_op
        self.cache = dict()
        self.key = key if key is not None else no_op
        self.properties = kwargs

    def __getitem__(self, obj):
        key = self.key(obj)
        if key not in self.cache:
            if self.parent:
                value, found = self.parent.get(key)
                if found:
                    return value
            self.cache[key] = self.factory(obj)
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
         state = self.__dict__.copy()
         del state['factory']
         return state
