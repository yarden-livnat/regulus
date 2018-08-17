def node_size(context, node):
    return node.data.size()

def node_relative_size(context, node):
    return node.data.size()/context['data_size']

def node_span(context, node):
    return node.parent.data.persistence - node.data.persistence
