from topopy.MorseSmaleComplex import MorseSmaleComplex as MSC
from regulus.topo.builder import Builder
from regulus.topo.hmsc import HMSC, Partition
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

    hmsc = HMSC(data)
    hmsc.tree = _visit(builder.root, None, hmsc)
    fake = Node(data=Partition(-1, 1, hmsc=hmsc))
    fake.add_child(hmsc.tree)
    
    return hmsc


def _visit(p, parent, hmsc):
    partition = Partition(p.id, p.persistence, p.span, [p.min_idx, p.max_idx], p.max_merge, hmsc)
    node = Node(data=partition, parent=parent)
    for child in p.children:
        _visit(child, node, hmsc)
    return node
