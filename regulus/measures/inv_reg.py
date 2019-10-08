from .null_model import NullModel
from sklearn.kernel_ridge import KernelRidge
import numpy as np
import pandas as pd


def radial_kernel(x0, X, tau):
    return np.exp(np.sum((X - x0) ** 2, axis=1) / (-2 * tau * tau))


def lowess(x0, X, Y, tau):
    # add bias term
    x0 = np.r_[1, x0]
    X = np.c_[np.ones(len(X)), X]
    # fit model: normal equations with kernel
    xw = X.T * radial_kernel(x0, X, tau)
    beta = np.linalg.pinv(xw @ X) @ xw @ Y

    # predict value
    return x0 @ beta


def inverse_regression(context, node):
    partition = node.data
    if partition.y.size < 2:
        return []
    



def inverse_ridge(context, node):
    partition = node.data
    if partition.y.size < 2:
        return NullModel()
    model = KernelRidge(alpha=1.0, kernel='rbf')
    model.fit(pd.DataFrame({'Y': partition.y}), partition.original_x)
    return model

def inverse_curve(context, node):
    if len(node.data.y) < 2:
        return []
    inv_model = context['inverse_ridge'][node]
    partition = node.data
    y = np.linspace(np.amin(partition.y), np.amax(partition.y), 100)
    x = inv_model.predict(pd.DataFrame({'Y': y}))
    return list(zip(x, y))
