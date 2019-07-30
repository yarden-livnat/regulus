from regulus.utils.cache import Cache
from regulus.models import NullModel
# from regulus.tree import reduce_tree Node
# from regulus.topo import Partition


def model_cache(model):
    return Cache(key=lambda n: n.data.id,
                 factory=lambda n: model(n.data) if n.data.id is not -1 else NullModel())


def compute_model(dataset, model, cache=None):
    if cache is None:
        cache = model_cache(model)

    for node in dataset.tree:
        cache[node] = model(node.data)
    return cache


# def compute_measure(dataset, measure, models, cache=None):
#     if cache is None:
#         cache = Cache()
#     for node in dataset.tree:
#         measure(node, cache, models)
#     return cache


def apply_model(model_name, model, regulus):
    regulus.attrs[model_name] = compute_model(model, regulus.tree)


def apply_measure(measure, tree):
    local = tree.attrs
    context = tree.regulus.attrs
    for node in tree:
        measure(node, local, context)


def compute_measure(func, tree):
    local = tree.attrs
    context = tree.regulus.attrs
    cache = dict()
    for node in tree:
        cache[node.id] = func(node, local, context)
    return cache
