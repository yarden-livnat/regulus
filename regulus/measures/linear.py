# def cache_key(*args):
#     if len(args) == 1:
#         return args[0].id
#     return f'{args[0].id}:{args[1].id}'
#
#
# def cached(name, key=cache_key):
#     def named(factory):
#         def wrapper(*args):
#             cache = args[-1][name]
#             k = key(*args)
#             if k not in cache:
#                 print('cache miss for ', name)
#                 cache[k] = factory(*args)
#             return cache[k]
#         return wrapper
#     return named


# @cached('fitness')
def fitness(context, node):
    return context['linear'][node].score(node.data.x, node.data.y)


# @cached('relative_fitness')
def relative_fitness(context, use_model, use_pts):
    return context['linear'][use_model].score(use_pts.data.x, use_pts.data.y)


# @cached('parent_fiteness')
def parent_fitness(context, node):
    if node.id == -1 or node.parent.id == -1:
        return 0
    return context['relative_fitness'][node.parent, node]


# @cached('child_fiteness')
def child_fitness(context, node):
    if node.id == -1 or node.parent.id == -1:
        return 0
    return context['relative_fitness'][node, node.parent]
