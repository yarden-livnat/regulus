import json
import csv
from pathlib import Path
from datetime import date
from getpass import getuser

DEFAULT_SAMPLE_METHOD = 'Predictor'


def from_csv(filename, ndims=-1, name=None, sample_method=DEFAULT_SAMPLE_METHOD, duplicates=True):
    with open(filename) as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [[float(x) for x in row] for row in reader]

        path = Path(filename)
        if name is None:
            name = path.stem

        regulus = {
            'name': name,
            'version': '1',
            'dims': header[0:ndims],
            'measures': header[ndims:],
            'notes': [{"date": str(date.today()), "author": getuser()}],
            'attr': {
                'path': str(path.with_suffix('.json'))
            },
            'sample_method': sample_method,
            'pts': data,
            'morse': {
                'params': {},
                'complexes': {}
            }
        }

        if duplicates:
            remove_duplicates(regulus)

        return regulus


def load(filename):
    with open(filename) as f:
        regulus = json.load(f)
        verify(regulus)
        return regulus


def get(spec=None, version=None, name=None, dir=None):
    if dir is not None:
        cur_dir = dir
    else:
        cur_dir = Path('.')

    if spec is not None:
        # spec is the file from
        name = spec['name']
        version = spec['version']
        get(name=name, version=version, dir=cur_dir)

    else:

        if (cur_dir / (name + '.' + version + '.json')).exists():
            regulus = load(cur_dir / (name + '.' + version + '.json'))

        elif (cur_dir / (name + '.json')).exists():
            regulus = load(cur_dir / (name + '.json'))

        else:
            print("Can not find old regulus file")

    return regulus


def save(regulus, filename=None, dir=None):
    if filename is None:
        filename = regulus['attr']['path']

    with open(filename, 'w') as f:
        json.dump(regulus, f, indent=2)


def remove_duplicates(regulus, force=False):
    import numpy as np
    from topopy.MorseSmaleComplex import TopologicalObject

    if not force and 'validated' in regulus['attr']:
        return

    pts = np.array(regulus['pts'])
    n = len(regulus['dims'])
    x = pts[:, 0:n]
    y = pts[:, n:]
    x, y = TopologicalObject.aggregate_duplicates(x, y)
    regulus['pts'] = np.concatenate((x, y), axis=1).tolist()
    regulus['attr']['validated'] = True


def params(regulus, measure=None):
    if measure is None:
        return regulus['morse']['params']
    if measure in regulus['morse']['complexes']:
        return regulus['morse']['complexes'][measure]['params']
    return {}


def verify(regulus):
    if 'attr' not in regulus:
        regulus['attr'] = {}

    if 'version' not in regulus:
        regulus['version'] = '1'

    attr = regulus['attr']
    if 'path' not in attr:
        # Changed to store version
        # attr['path'] = regulus['name']+'.json'
        attr['path'] = regulus['name'] + regulus['version'] + '.json'

    if 'sample_method' not in regulus:
        regulus['sample_method'] = DEFAULT_SAMPLE_METHOD
