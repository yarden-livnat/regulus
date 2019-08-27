import pickle

from pathlib import Path
from time import process_time

from regulus.data.data import Data
from regulus.topo import msc, Regulus
from regulus.measures import *
from regulus.models import *
from regulus.alg import AttrRange


def load(filename):
    path = Path(filename).with_suffix('.regulus')
    with open(path, 'rb') as f:
        t = pickle.load(f)
        if isinstance(t, Regulus):
            t.filename = path
            return t
        raise Exception('file %1 is not a Regulus file'.format(filename))


def save(regulus, filename=None):
    if filename is None and regulus.filename is None:
        raise(Exception("Filename must be provide when the Regulus object doesn't have a default filename"))

    if filename is None:
        filename = regulus.filename
    path = Path(filename).with_suffix('.regulus')
    if regulus.filename is None:
        regulus.filename = path

    with open(path, 'wb') as f:
        pickle.dump(regulus, f)


def add_defaults(regulus):
    regulus.add_attr(linear_model, name='linear')
    regulus.add_attr(fitness, range=AttrRange('fixed', [0,1]))
    regulus.add_attr(relative_fitness, range=AttrRange('fixed', [0,1]))
    regulus.add_attr(stepwise_fitness)
    regulus.add_attr(node_min, name='min', range=AttrRange('auto'))
    regulus.add_attr(node_max, name='max', range=AttrRange('auto'))

    regulus.tree.add_attr(parent_fitness, range=AttrRange('fixed', [0,1]))
    regulus.tree.add_attr(child_fitness, range=AttrRange('fixed', [0,1]))
    regulus.tree.add_attr(node_size, name='size', range=AttrRange('auto'))
    regulus.tree.add_attr(node_relative_size, name='rel_size', range=AttrRange('fixed', [0,1]))
    regulus.tree.add_attr(node_span, name='span', range=AttrRange('fixed', [0,1]))


def from_csv(filename, **kwargs):
    t_start = process_time()
    path = Path(filename)
    ndims = kwargs.pop('ndims', None)
    pts = Data.read_csv(path.with_suffix('.csv'), ndims=ndims)
    t_read = process_time()

    pts.normalize()
    regulus = msc(pts, **kwargs)
    t_msc = process_time()

    add_defaults(regulus)

    # save(regulus, filename=path.with_suffix('.regulus'))
    t_end = process_time()
    print(f'time: {t_end - t_start:.3} read:{t_read-t_start:.3} msc:{t_msc-t_read:.3}  save:{t_end-t_msc:.3}')
    return regulus


def from_df(pts, **kwargs):
    t_start = process_time()
    pts.normalize()
    regulus = msc(pts, **kwargs)
    add_defaults(regulus)

    t_end = process_time()
    print(f'time: {t_end - t_start:.3}')
    return regulus
