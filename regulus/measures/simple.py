def cache_key(*args):
    return args[0].ref

def cache_key2(*args):
    return f'{args[0].ref}:{args[1].ref}'


def cached(name, key=cache_key):
    def named(measure):
        def wrapper(*args):
            cache = args[-1][name]
            k = key(*args)
            if k not in cache:
                print('cache miss')
                cache[k] = measure(*args)
            return cache[k]
        return wrapper
    return named


# @cached('fitness')
def fitness(node, context):
    print('fitness for', node.ref)
    return context['linear'][node].score(node.data.x, node.data.y)


@cached('relative_fitness', key=cache_key2)
def relative_fitness(use_model, use_pts, context):
    print('relative fitness for', use_model.ref, use_pts.ref)
    return context['linear'][use_model].score(use_pts.data.x, use_pts.data.y)


# @cached('parent_fiteness')
def parent_fitness(node, context):
    print('parent fitness for', node.ref)
    return relative_fitness(node.parent, node, context)


# @cached('child_fiteness')
def child_fitness(node, context):
    print('child for', node.ref)
    return relative_fitness(node, node.parent, context)
