import pickle
from pathlib import Path
from time import process_time

from regulus.data.data import Data
from regulus.topo import morse_smale, Regulus
from regulus.measures import *
from regulus.models import *


def load(filename):
    with open(filename, 'rb') as f:
        t = pickle.load(f)
        if isinstance(t, Regulus):
            t.filename = filename
            return t
        raise Exception('file %1 is not a Topology file'.format(filename))


def save(topology, filename=None):
    if topology.filename is None:
        topology.filename = filename
    if filename is None:
        filename = topology.filename

    with open(filename, 'wb') as f:
        pickle.dump(topology, f)


def from_csv(filename, **kwargs):
    t_start = process_time()
    ndims = kwargs.pop('ndims', None)
    pts = Data.read_csv(f'{filename}.csv',ndims=ndims)
    t_read = process_time()

    pts.normalize()
    regulus = morse_smale(pts, **kwargs)
    t_msc = process_time()

    regulus.add_attr('linear', linear_model)
    regulus.add_attr('fitness', fitness)
    regulus.add_attr('relative_fitness', relative_fitness)

    regulus.tree.add_attr('parent_fitness', parent_fitness)
    regulus.tree.add_attr('child_fitness', child_fitness)
    regulus.tree.add_attr('size', node_size)
    regulus.tree.add_attr('rel_size', node_relative_size)
    regulus.tree.add_attr('span', node_span)

    save(regulus, filename=f'{filename}.p')
    t_end = process_time()
    print(f'time: {t_end - t_start:.3} read:{t_read-t_start:.3} msc:{t_msc-t_read:.3}  save:{t_end-t_msc:.3}')
    return regulus
