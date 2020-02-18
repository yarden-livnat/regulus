import random

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


def unique_id(context, id):
    '''assign a random  number for an id'''
    return random.uniform(0,1)


def unique_max(tree, node):
    id = node.data.minmax_idx[1]
    return tree['unique_id'][id]


def unique_min(tree, node):
    id = node.data.minmax_idx[0]
    return tree['unique_id'][id]