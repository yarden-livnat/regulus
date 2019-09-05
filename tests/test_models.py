import argparse
from regulus.tree.traverse import *
from regulus.utils import io

from sklearn import linear_model

p = argparse.ArgumentParser()
p.add_argument('filename', help='input file')

ns = p.parse_args()

t = io.load(ns.filename)

for node in traverse(t.tree):
    p = node.data
    model = linear_model.LinearRegression()
    model.fit(p.x, p.y)
    p.models['fwd'] = model


# for node in traverse(t.tree):
#     p = node.data
#     p.measures['fwd_fitness'] = p.models['fwd'].score(p.x, p.y)
#     print(p.id, 'score', p.measures['fwd_fitness'])

for p in t.tree.items():
    p.measures['fwd_fitness'] = p.models['fwd'].score(p.x, p.y)
    print(p.id, 'score', p.measures['fwd_fitness'])