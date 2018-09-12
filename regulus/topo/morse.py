from types import SimpleNamespace
import pandas as pd
from topopy.MorseSmaleComplex import MorseSmaleComplex as MSC
from topopy.TopologicalObject import TopologicalObject

from regulus.topo.builder import Builder
from regulus.topo import Regulus, Partition, RegulusTree
from regulus.tree import Node

defaults = SimpleNamespace(
        knn=100,
        beta=1,
        norm=None,
        graph='relaxed beta skeleton',
        gradient='steepest',
        aggregator= 'mean'
)

def morse_smale(data, measure=None, knn=defaults.knn, beta=defaults.beta, norm=defaults.norm, graph=defaults.graph,
                gradient=defaults.gradient, aggregator=defaults.aggregator, debug=False):

    if measure is None:
        measure = list(data.values.columns)[-1]
    if type(measure) == int:
        measure = list(data.values.columns)[measure]

    x, values = TopologicalObject.aggregate_duplicates(data.x.values, data.values.values)
    if x.shape != data.x.shape:
        data.x = pd.DataFrame(x, columns=data.x.columns)
        data.values = pd.DataFrame(values, columns=data.values.columns)

    y = data.values.loc[:, measure]

    """Compute a Morse-Smale Complex"""
    msc = MSC(graph=graph, gradient=gradient, max_neighbors=knn, beta=beta, normalization=norm, aggregator=aggregator)
    msc.build(X=data.x.values, Y=y, names=list(data.x.columns) + [y.name])

    builder = Builder(debug).data(y).msc(msc.base_partitions, msc.hierarchy)
    builder.build()
    if debug:
        builder.verify()

    regulus = Regulus(data, builder.pts, measure)
    regulus.tree.root  = _visit(builder.root, None, regulus, 0)
    return regulus


def _visit(p, parent, regulus, offset):
    partition = Partition(p.id, p.persistence, p.span, [p.min_idx, p.max_idx], p.max_merge, regulus)
    node = Node(ref=partition.id, data=partition, parent=parent, offset=offset)
    for child in p.children:
        _visit(child, node, regulus, offset)
        offset += child.span[1] - child.span[0]
    return node
