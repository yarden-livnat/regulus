from regulus.utils import io
from regulus.tree import *

gauss = io.load('gauss4')

tree = gauss.tree

def f(c, n):
    attr = c.attr['fitness']
    value = attr[n]
    return value > 0.4


r = tree.reduce(filter=f)

print('\treduced')
for node, depth in traverse(r.root, depth=True):
    print('.'*depth,node.ref)
