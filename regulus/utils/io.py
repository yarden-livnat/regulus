import pickle
from pathlib import Path
from regulus.data.data import Data
from regulus.topo import morse_smale, Regulus

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


def morse_from_csv(filename, ndims=None, measure=None, save=False, **kwargs):
    p = Path(filename)
    data = Data.read_csv(filename, ndims, measure)
    data.normalize()
    msc = morse_smale(data, **kwargs)
    msc.filename = p.with_suffix('.p')
    if save:
        if not isinstance(save, str):
            save = None
        io.save(msc, filename=save)
    return msc
