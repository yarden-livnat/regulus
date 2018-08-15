from topopy.MorseSmaleComplex import MorseSmaleComplex as MSC
from regulus.topo.builder import Builder
from regulus.topo import Regulus, Partition, RegulusTree
from regulus.tree import Node


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

    regulus = Regulus(data)
    regulus.tree.root  = _visit(builder.root, None, regulus, 0)
    return regulus


def _visit(p, parent, regulus, offset):
    partition = Partition(p.id, p.persistence, p.span, [p.min_idx, p.max_idx], p.max_merge, regulus)
    node = Node(ref=partition.id, data=partition, parent=parent, offset=offset)
    for child in p.children:
        _visit(child, node, regulus, offset)
        offset += child.span[1] - child.span[0]
    return node
