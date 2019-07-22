def node_size(context, node):
    return node.data.size()

def node_relative_size(context, node):
    return node.data.size()/context['data_size']

def node_span(context, node):
    return node.parent.data.persistence - node.data.persistence

def node_max(context, node):
    return node.data.max()

def node_min(context, node):
    return node.data.min()
