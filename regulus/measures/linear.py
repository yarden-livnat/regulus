import numpy as np
from sklearn import linear_model as lm
from sklearn.metrics.pairwise import cosine_similarity


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


def relative_fitness(context, has_model, has_pts):
    if len(has_pts.data.y) < 2:
        return 0
    return context['linear'][has_model].score(has_pts.data.x, has_pts.data.y)


def parent_fitness(context, node):
    if node.id == -1 or node.parent.id == -1:
        return 0
    return context['relative_fitness'][node.parent, node]


def child_fitness(context, node):
    if node.id == -1 or node.parent.id == -1:
        return 0
    return context['relative_fitness'][node, node.parent]


def dim_scores(context, node):
    partition = node.data
    if partition.y.size < 2:
        return [0] * len(partition.x.columns)

    models = context['dim_models'][node]
    return [m.score(partition.x[[d]], partition.y) for m, d in zip(models, partition.x.columns)]


def dim_min_fitness(context, node):
    return min(context['dim_scores'][node])


def dim_max_fitness(context, node):
    return max(context['dim_scores'][node])


def relative_dim_score(context, has_models, has_points):
    if len(has_points.data.y) < 2:
        return [0] * len(has_points.data.x.columns)

    models = context['dim_models'][has_models]
    return [m.score(has_points.data.x[[d]], has_points.data.y) for m, d in zip(models, has_points.data.x.columns)]


def dim_parent_score(context, node):
    v = cosine_similarity(
            [context['dim_scores'][node]],
            [context['relative_dim_score'][node.parent, node]])
    return v[0][0]


def dim_child_score(context, node):
    v = cosine_similarity(
        [context['dim_scores'][node]],
        [context['relative_dim_score'][node, node.parent]])
    return v[0][0]
