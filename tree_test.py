from regulus.tree.traverse import *


class TestNode(Node):
    def __init__(self, **kwargs):
        super(TestNode, self).__init__(**kwargs)

    def __str__(self):
        if self.data is None:
            return "<none>"
        return self.data

def show(root):
    for node in depth_first(root):
        print(node.data)


def show_depth(root, depth=0):
    print('{}{} d={}'.format(' '*depth, str(root), depth))
    for child in root.children:
        show_depth(child, depth+1)


root = TestNode(data='root')
n1 = TestNode(data='.1',parent=root)
n2 = TestNode(data='.2',parent=root)

n11 = TestNode(data='.1.1',parent=n1)
n12 = TestNode(data='.1.2',parent=n1)

n21 = TestNode(data='.2.1',parent=n2)
n211 = TestNode(data='.2.1.1',parent=n21)
n212 = TestNode(data='.2.1.2',parent=n21)
n22 = TestNode(data='.2.2',parent=n2)


print('breath first. pre')
for n in breath_first(root):
    print(n.data)

print('breath first. post')
for n in breath_first(root, post=True):
    print(n.data)


print('breath first. both')
for n in breath_first(root, both=True):
    print(n.data)


print('depth first. pre')
for n in depth_first(root):
    print(n.data)

print('depth first. post')
for n in depth_first(root, post=True):
    print(n.data)


values = dict([('root', 2),
               ('.1', 5),
               ('.1.1', 15),
               ('.1.2', 3),
               ('.2', 6),
               ('.2.1', 20),
               ('.2.2', 9),
               ('.2.1.1', 0),
               ('.2.1.2', 30),
               ])


print('best first')
for v, n in best_first(root, value=lambda n: values[n.data]):
    print(v, n.data)


print('reduce .1')
x = reduce(root, lambda n: '.1' in n.data, factory=TestNode)
show_depth(x)

print('reduce .2')
x = reduce(root, lambda n: '.2' in n.data, factory=TestNode)
show_depth(x)