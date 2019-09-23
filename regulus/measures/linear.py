import numpy as np
from sklearn import linear_model as lm


def fitness(context, node):
    if len(node.data.y) < 2:
        return 0
    return context['linear'][node].score(node.data.x, node.data.y)


def stepwise_fitness(context, node):
    fitness = []
    coefficients = np.fabs(context['linear'][node].coef_)
    sorted_dims = np.argsort(coefficients)
    for i in range(len(sorted_dims)):
        subspace = sorted_dims[:(i+1)]
        model = lm.LinearRegression()
        X = node.data.x[:, subspace]
        Y = node.data.y
        model.fit(X, Y)
        fitness.append((sorted_dims[i], model.score(X, Y)))
    return fitness


def relative_fitness(context, has_mode, has_pts):
    if len(has_pts.data.y) < 2:
        return 0
    return context['linear'][has_mode].score(has_pts.data.x, has_pts.data.y)


def parent_fitness(context, node):
    if node.id == -1 or node.parent.id == -1:
        return 0
    return context['relative_fitness'][node.parent, node]


def child_fitness(context, node):
    if node.id == -1 or node.parent.id == -1:
        return 0
    return context['relative_fitness'][node, node.parent]
