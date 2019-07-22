def quadratic_fitness(context, node):
    return context['quadratic'][node].score(node.data.x, node.data.y)
