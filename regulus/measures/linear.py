# def cache_key(*args):
#     if len(args) == 1:
#         return args[0].ref
#     return f'{args[0].ref}:{args[1].ref}'
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
    # print('fitness for', node.ref)
    return context['linear'][node].score(node.data.x, node.data.y)


# @cached('relative_fitness')
def relative_fitness(context, use_model, use_pts):
    # print('relative fitness for', use_model.ref, use_pts.ref)
    return context['linear'][use_model].score(use_pts.data.x, use_pts.data.y)


# @cached('parent_fiteness')
def parent_fitness(context, node):
    if node.ref == -1 or node.parent.ref == -1:
        return 1
    # print('parent fitness for', node.ref)
    # return relative_fitness(node.parent, node, context)
    return context['relative_fitness'][node.parent, node]


# @cached('child_fiteness')
def child_fitness(context, node):
    # print('child for', node.ref)
    # return relative_fitness(node, node.parent, context)
    if node.ref == -1 or node.parent.ref == -1:
        return 1
    return context['relative_fitness'][node, node.parent]
