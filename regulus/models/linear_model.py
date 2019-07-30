from .null_model import NullModel
from sklearn import linear_model as lm


def linear_model(context, node):
    partition = node.data
    if partition.y.size < 2:
        return NullModel()
    model = lm.LinearRegression()
    model.fit(partition.x, partition.y)
    return model
