

def fitness(node, cache, models):
    key = 'fitness:{}'.format(node.data.id)
    if key not in cache:
        # print(key)
        cache[key] = models[node].score(node.data.x, node.data.y)
    return cache[key]


def relative_fitness(use_model, use_pts, cache, models):
    key = 'relative_fitness:{}:{}'.format(use_model.data.id, use_pts.data.id)
    if key not in cache:
        # print(key)
        cache[key] = models[use_model].score(use_pts.data.x, use_pts.data.y)
    return cache[key]


def parent_fitness(node, cache, models):
    return relative_fitness(node.parent, node, cache, models)


def child_fitness(node, cache, models):
    return relative_fitness(node, node.parent, cache, models)
