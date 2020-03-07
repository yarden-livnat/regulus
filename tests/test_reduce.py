import regulus


def test(t1, t2):
    print('=== test 1')
    n1 = t1.find_id(64)
    a1 = t1.attr[attr][n1]
    print('a1', a1)

    print('==== test 2')
    n2 = t2.find_id(64)
    a2 = t2.attr[attr][n2]
    print('a2', a2)


compute = True

if compute:
    data = regulus.from_csv('gauss4', knn=8)
else:
    data = regulus.load('gauss4')

t1 = data.tree

rt = regulus.ReduceTree(filter=lambda context, node: node.parent.data.persistence - node.data.persistence > 0.15)
rt.src = t1
t2 = rt.tree

print('-----')
print('t1 id:', id(t1))
print('t2 id:', id(t2))
print('-----')

print(f't1: {t1.size()}  t2: {t2.size()}')

print(f't1 parent: {t1.find_id(64).parent.id}')

print(f't2 parent: {t2.find_id(64).parent.id}')

attr = 'child_fitness'

# test(t1, t2)
test(t2, t1)




