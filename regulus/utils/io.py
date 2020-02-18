import pickle

from pathlib import Path
from time import process_time

from regulus.core.data import Data
from regulus.topo import msc, Regulus
from regulus.measures import *
from regulus.models import *
from regulus.core import UNIT_RANGE


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
    regulus.add_attr(fitness, range=UNIT_RANGE)
    regulus.add_attr(relative_fitness, range=UNIT_RANGE)
    regulus.add_attr(stepwise_fitness)
    regulus.add_attr(node_min, name='min')
    regulus.add_attr(node_max, name='max')

    regulus.add_attr(unique_id, range=UNIT_RANGE)
    regulus.add_attr(unique_max, range=UNIT_RANGE)
    regulus.add_attr(unique_min, range=UNIT_RANGE)

    regulus.add_attr(dim_models)

    regulus.add_attr(dim_scores)
    regulus.add_attr(dim_min_fitness)
    regulus.add_attr(dim_max_fitness)
    regulus.add_attr(relative_dim_score)
    regulus.add_attr(dim_parent_score)
    regulus.add_attr(dim_child_score)

    regulus.add_attr(default_inverse_regression, name='inverse_regression')

    regulus.tree.add_attr(parent_fitness, range=UNIT_RANGE)
    regulus.tree.add_attr(child_fitness, range=UNIT_RANGE)
    regulus.tree.add_attr(node_size, name='size')
    regulus.tree.add_attr(node_relative_size, name='rel_size', range=UNIT_RANGE)
    regulus.tree.add_attr(node_span, name='span', range=UNIT_RANGE)


def from_csv(filename, **kwargs):
    path = Path(filename)
    if not path.exists():
        if path.suffix == '':
            if not path.with_suffix('.csv').exists():
                raise FileNotFoundError(f"File '{filename}[.csv]' does not exist")

    t_start = process_time()
    ndims = kwargs.pop('ndims', None)
    pts = Data.read_csv(path.with_suffix('.csv'), ndims=ndims)
    t_read = process_time()

    if kwargs.pop('normalize', True):
        pts.normalize()
    regulus = msc(pts, **kwargs)
    t_msc = process_time()

    add_defaults(regulus)

    t_end = process_time()
    if kwargs.get('debug', False):
        print(f'time: {t_end - t_start:.3} ')
    return regulus


def from_df(df, **kwargs):
    t_start = process_time()
    pts = Data.from_df(df, ndims = kwargs.pop('ndims', None))
    if kwargs.pop('normalize', True):
        pts.normalize()
    regulus = msc(pts, **kwargs)
    add_defaults(regulus)

    t_end = process_time()
    if kwargs.get('debug', False):
        print(f'time: {t_end - t_start:.3}')
    return regulus
