import regulus as r

print('pickle 1')
# from importlib import import_module
#
# module = import_module('bar')
# if hasattr(module, 'node_id'):
#     node_id = getattr(module, 'node_id')
# else:
#     node_id = lambda c, n: None

# data = r.from_csv('gauss4', knn=8)
#
#
# node = data.tree.find_id(4)
#
# f = data.attr['fitness'][node]
# print('span', f)
#
# pf = data.tree.attr['parent_fitness'][node]
# print('parent fitness', pf)
#
# # data.add_attr(lambda c,n: n.id, 'node-id')
# # v = data.attr['node-id'][node]
# # print('node-id', v)
#
#
# def node_id(c,n):
#     return n.id
#
#
# data.add_attr(node_id)
# v = data.attr['node_id'][node]
# print('node-id', v)
#
# r.save(data, filename='foo')



foo = r.load('foo')
node = foo.tree.find_id(14)
v = foo.attr['node_id'][node]
# v = node_id(None, node)
print('foo node-id', v)