from .null_model import NullModel
from sklearn import linear_model as lm


def linear_model(context, node):
    partition = node.data
    if partition.y.size < 2:
        return NullModel()
    model = lm.LinearRegression()
    model.fit(partition.x, partition.y)
    return model


def ridge_model(context, node):
    if node.id < 0 or node.data.y.size < 2:
        return NullModel()
    model = lm.Ridge(alpha=1.0)
    model.fit(node.data.x, node.data.y)
    return model


def shared_model(context, node):
    return context['model'][node]


def model_of(klass, **kwargs):
    def _create(context, node):
        partition = node.data
        if partition.y.size < 2:
            return
        model = klass(**kwargs)
        model.fit(partition.x, partition.y)
        return model

    return _create


def dim_model(context, node):
    partition = node.data
    if partition.y.size < 2:
        return [NullModel() for d in partition.x.columns]

    models = [lm.Ridge().fit(partition.x[[d]], partition.y) for d in partition.x.columns]
    return models
