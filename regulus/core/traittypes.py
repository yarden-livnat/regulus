from traitlets import TraitType


class Function(TraitType):
    default_value = lambda *args, **kwargs: None
    info_text = 'a callable object'

    def _validate(self, obj, value):
        if value is None or callable(value):
            return value
        self.error(obj, value)
