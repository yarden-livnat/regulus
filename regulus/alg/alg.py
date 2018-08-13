from .cache import Cache
from regulus.models import NullModel

class ModelCache(Cache):
    def __init__(self, factory):
        super().__init__(key=lambda n: n.data.id,
                         factory=lambda n: factory(n.data) if n.data.id is not -1 else NullModel())


def compute_model(dataset, model, cache=None):
    if cache is None:
        cache = ModelCache(model)

    for node in dataset.tree:
        cache[node] = model(node.data)
    return cache


def compute_measure(dataset, measure, models, cache=None):
    if cache is None:
        cache = Cache()
    for node in dataset.tree:
        measure(node, cache, models)
    return cache
