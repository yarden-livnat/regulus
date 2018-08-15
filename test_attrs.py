from regulus.utils import io
from regulus.topo import *
from regulus.alg import *
from regulus.measures.simple import *
from regulus.models import *
from regulus.tree import *


gauss = io.load('data/gauss4.p')

gauss.add_attr('linear', lambda n, context: linear_model(n.data) if n.ref is not -1 else NullModel)
gauss.attrs['relative_fitness'] = {}

gauss.add_attr('fitness', fitness)
# gauss.add_attr('relative_fitness', relative_fitness)

gt = gauss.tree
g_root = gt.root
g_n1 = g_root.children[0]
g_n2 = g_root.children[1]

gt.add_attr('parent_fitness', parent_fitness)

nt = reduce(gt, filter=lambda n: n.data.size() > 100)
n_root = nt.root
n_n1 = n_root.children[0]
n_n2 = n_root.children[1]

print('g_root == n_root', g_root == n_root)
print('g_n1 == n_n1', g_n1 == n_n1)
print('g_n2 == n_n2', g_n2 == n_n2)

print('g root fitness=', gt.attrs['fitness'][g_root])
print('n root fitness=', nt.attrs['fitness'][nt.root])


print('g_n1 parent_fitness=', gt.attrs['parent_fitness'][g_n1])
print('n_n1 parent_fitness=', nt.attrs['parent_fitness'][n_n1])