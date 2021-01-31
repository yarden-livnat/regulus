from types import SimpleNamespace
from topopy.MorseSmaleComplex import MorseSmaleComplex
import nglpy as ngl

from regulus.topo.builder import Builder
from regulus.topo import Regulus, Partition
from regulus.tree import Node

defaults = SimpleNamespace(
        knn=100,
        beta=1,
        norm=None,
        graph='relaxed beta skeleton',
        gradient='steepest',
        aggregator=None
)


def msc(data, kind='smale', measure=None, knn=defaults.knn, beta=defaults.beta, norm=defaults.norm,
        graph=defaults.graph, gradient=defaults.gradient, aggregator=defaults.aggregator,
        debug=False):
    """Compute a Morse-Smale Complex"""

    if measure is None:
        measure = list(data.values.columns)[-1]
    elif type(measure) == int:
        measure = list(data.values.columns)[measure]

    # TODO: that's an unexpected side-effect.
    #       either make the user do this step outside of this function or
    #       provide a parameter to explicitly ask for that
    # topopy ver 1.0: comment out. Is this correct?
    # x, values = TopologicalObject.aggregate_duplicates(data.x.values, data.values.values)
    # if x.shape != data.x.shape:
    #     data.x = pd.DataFrame(x, columns=data.x.columns)
    #     data.values = pd.DataFrame(values, columns=data.values.columns)

    y = data.values.loc[:, measure]

    if 'knn' in graph:
        beta=0.0
        relaxed = True
    else:
        relaxed = 'relaxed' in graph
        
    ngl_graph = ngl.EmptyRegionGraph(max_neighbors=knn, relaxed=relaxed, beta=beta, p=2.0)    
    topo = MorseSmaleComplex(graph=ngl_graph, gradient=gradient, normalization=norm, aggregator=aggregator)
    topo.build(X=data.x.values, Y=y.values)

    builder = Builder(debug).data(y)

    # if kind == 'smale':
    #     builder.msc(topo.base_partitions, topo.hierarchy)
    # elif kind == 'descend':
    #     builder.msc(topo.descending_partitions, topo.max_hierarchy)
    # else:
    #     builder.msc(topo.ascending_partitions, topo.min_hierarchy)

    builder.msc(topo.base_partitions, topo.get_merge_sequence())

    builder.build()

    regulus = Regulus(data, builder.pts, measure, type=kind)
    regulus.tree.root = _visit(builder.root, None, regulus, 0)

    return regulus


def _visit(p, parent, regulus, offset):
    partition = Partition(p.id,
                          p.persistence,
                          pts_span=p.span,
                          minmax_idx=[p.min_idx, p.max_idx],
                          extrema=p.extrema,
                          max_merge=p.max_merge,
                          base=p.base,
                          regulus=regulus)
    node = Node(ref=partition.id, data=partition, parent=parent, offset=offset)
    for child in p.children:
        _visit(child, node, regulus, offset)
        offset += child.span[1] - child.span[0]
    return node


def morse_smale(data, **kwargs):
    return msc(data, kind='smale', **kwargs)


def morse(data, type='descend', **kwargs):
    return msc(data, type, **kwargs)
