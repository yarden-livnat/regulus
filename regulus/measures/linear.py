
def fitness(node, _, context):
    cache = context['fitness']
    key = node.ref
    if key not in cache:
        cache[key] = context['linear'][node].score(node.data.x, node.data.y)
    return cache[key]

def relative_fitness(use_model, use_pts, _, context):
    if use_model.ref == -1 or use_pts.ref == -1:
        return 1
    key = '{}.{}'.format(use_model.ref, use_pts.ref)
    cache = context['relative_fitness']
    if key not in cache:
        cache[key] = context['linear'][use_model].score(use_pts.data.x, use_pts.data.y)
    return cache[key]

def parent_fitness(node, local, context):
    cache = local['parent_fitness']
    if node.ref not in cache:
        if node.parent.ref == -1:
            cache[node.ref] = 1
        else:
            cache[node.ref] = relative_fitness(node.parent, node, cache, context)
    return cache[node.ref]


def child_fitness(node, local, context):
    cache = local['child_fitness']
    if node.ref not in cache:
        if node.parent.ref == -1:
            cache[node.ref] = 1
        else:
            cache[node.ref] = relative_fitness(node, node.parent, cache, context)
    return cache[node.ref]
