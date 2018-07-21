import sys
import argparse

from regulus import file as rf
from .morse import morse
from typing import Iterable


def parse_args(args=None):
    p = argparse.ArgumentParser(prog='morse', description='compute Morse (or Morse-Smale complex')
    p.add_argument('filename', help='regulus .json file]')

    p.add_argument('-k', '--knn', type=int, help='knn')
    p.add_argument('-b', '--beta', type=float, help='beta')
    p.add_argument('-n', '--norm', help='norm')
    p.add_argument('-g', '--graph', nargs='*', help='graph')
    p.add_argument('-G', '--gradient', help='gradient')

    p.add_argument('-m', '--measures', nargs='*', default=None, help='measures to process. default=all measures')

    p.add_argument('-t', '--type', default='smale', choices=['smale', 'ascend', 'descend'],
                   help='type of complex to compute')
    p.add_argument('-o', '--out', help='output file')
    p.add_argument('--debug', action='store_true', help='process all measures')

    return p.parse_args(args)


def run():
    ns = parse_args()
    regulus = rf.load(ns.filename)
    params = {}
    for a in ('knn', 'beta', 'norm', 'graph', 'gradient'):
        if hasattr(ns, a):
            params[a] = ' '.join(getattr(ns, a)) if isinstance(getattr(ns, a), Iterable) else getattr(ns, a)

    morse(regulus, kind=ns.type, measures=ns.measures, args=params, debug=ns.debug)

    filename = ns.out if ns.out is not None else ns.filename
    rf.save(regulus, filename)


if __name__ == 'main':
    run()