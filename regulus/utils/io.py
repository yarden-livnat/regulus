import pickle

from regulus.topo.hierarchical_complex import HierarchicalComplex


def load(filename):
    with open(filename, 'rb') as f:
        t = pickle.load(f)
        if isinstance(t, HierarchicalComplex):
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
