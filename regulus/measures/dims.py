from sklearn.metrics.pairwise import cosine_similarity


def dim_score(context, node):
    partition = node.data
    if partition.y.size < 2:
        return [0] * len(partition.x.columns)

    models = context['dim_model'][node]
    return [m.score(partition.x[[d]], partition.y) for m, d in zip(models, partition.x.columns)]


def dim_min(context, node):
    return min(context['dim_score'][node])


def dim_max(context, node):
    return max(context['dim_score'][node])


def dim_relative(context, has_models, has_points):
    if len(has_points.data.y) < 2:
        return [0] * len(has_points.data.x.columns)

    models = context['dim_model'][has_models]
    return [m.score(has_points.data.x[[d]], has_points.data.y) for m, d in zip(models, has_points.data.x.columns)]


def dim_parent(context, node):
    v = cosine_similarity(
            [context['dim_score'][node]],
            [context['dim_relative'][node.parent, node]])
    return v[0][0]


def dim_child(context, node):
    v = cosine_similarity(
        [context['dim_score'][node]],
        [context['dim_relative'][node, node.parent]])
    return v[0][0]
