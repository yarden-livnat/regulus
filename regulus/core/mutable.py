from traitlets import HasTraits, Int


class Mutable(HasTraits):
    version = Int(0)

    def invalidate(self):
        self.version += 1



