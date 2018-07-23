import pickle

from regulus.topo.topology import Topology


def load(filename):
    with open(filename, 'rb') as f:
        t = pickle.load(f)
        if isinstance(t, Topology):
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