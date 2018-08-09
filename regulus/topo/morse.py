from topopy.MorseSmaleComplex import MorseSmaleComplex as MSC
from regulus.topo.builder import Builder
from regulus.topo.hierarchical_complex import HierarchicalComplex, Partition
from regulus.tree.tree import Node


def morse_smale(data, knn=100, beta=1.0, norm=None, graph='relaxed beta skeleton', gradient='steepest',
                aggregator="mean", debug=False):
    """Compute a Morse-Smale Complex"""
    msc = MSC(graph=graph, gradient=gradient, max_neighbors=knn, beta=beta, normalization=norm, aggregator=aggregator)
    msc.build(X=data.x.values, Y=data.y.values, names=list(data.x.columns) + [data.y.name])
    x = msc.X
    y = msc.Y
    builder = Builder(debug).data(y).msc(msc.base_partitions, msc.hierarchy)
    builder.build()
    if debug:
        builder.verify()

    topology = HierarchicalComplex(data)
    topology.root = _visit(builder.root, None, topology)
    # topology.partitions = dict()
    # topology.tree.reduce(collect, topology.partitions)

    return topology


def _visit(p, parent, topology):
    partition = Partition(p.id, p.persistence, p.span, [p.min_idx, p.max_idx], p.max_merge, topology)
    node = Node(data=partition, parent=parent)
    for child in p.children:
        _visit(child, node, topology)
    return node


# def collect(node, partitions):
#     partitions[node.id] = node.partition
#     return partitions


