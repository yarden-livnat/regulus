import regulus


def stat(tree):
    for node, depth in regulus.traverse(tree.root, depth=True):
        print('.'*depth,node.id)

def f(c, n):
    attr = c.attr['fitness']
    value = attr[n]
    return value > 0.4


gauss = regulus.load('gauss4')
tree = gauss.tree

print('original')
stat(tree)

s = regulus.SimplifiedTree(tree, f)

print('reduced')
stat(s.tree)


