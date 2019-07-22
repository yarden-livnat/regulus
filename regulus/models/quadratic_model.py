from .null_model import NullModel
from sklearn.linear_model import  LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def quadratic_model(context, node):
    partition = node.data
    if partition.y.size < 2:
        return NullModel()
    model = make_pipeline(PolynomialFeatures(2),
                          LinearRegression())
    model.fit(partition.x, partition.y)
    return model
