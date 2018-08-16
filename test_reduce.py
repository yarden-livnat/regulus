from regulus.utils import io
from regulus.topo import *
from regulus.alg import *
from regulus.measures.linear import *
from regulus.models import *
from regulus.tree import *

gauss = io.load('data/gauss4.p')
gauss.add_attr('linear', node_model(linear_model))
gauss.add_attr('fitness', fitness)
gauss.add_attr('relative_fitness', relative_fitness)
gauss.tree.add_attr('parent_fitness', parent_fitness)
gauss.tree.add_attr('child_fitness', child_fitness)


tree = gauss.tree


r = reduce(tree, filter=lambda n: tree.attr['fitness'][n] > 0.4 )

print('\treduced')
for node, depth in traverse(r.root, depth=True):
    print('.'*depth,node.ref)
