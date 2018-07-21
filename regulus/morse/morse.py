import numpy as np

from topopy.MorseSmaleComplex import MorseSmaleComplex as MSC
from regulus import file as rf
from .post import Post

defaults = {
    'knn': 100,
    'beta': 1.0,
    'norm': 'feature',
    'graph': 'relaxed beta skeleton',
    'gradient': 'steepest'
}


def merge(src, default):
    if src is not None:
        dest = dict(src)
        for key, value in default.items():
            if key not in dest or dest[key] is None:
                dest[key] = default[key]
            print('merge', key, dest[key])
        return dest
    else:
        return default


def morse(regulus, kind=None, measures=None, args=None, debug=False):
    ndims = len(regulus['dims'])
    if measures is None:
        measures = regulus['measures']

    pts = np.array(regulus['pts'])
    x = pts[:, 0:ndims]

    for measure in measures:
        try:
            print('\nmeasure:', measure)
            i = regulus['measures'].index(measure)
            prev = rf.params(regulus, measure)
            params = merge(args, prev)

            current = merge(params, defaults)
            y = pts[:, ndims + i]

            msc = MSC(current['graph'], current['gradient'], current['knn'], current['beta'], current['norm'],
                      aggregator='mean')  # connect=True
            msc.build(X=x, Y=y, names=regulus['dims'] + [measure])

            x = msc.X
            y = msc.Y
            post = Post(debug).data(y)

            if kind is None:
                kind = regulus['morse']['complexes'][measure]['type']

            if kind == 'descend':
                post.msc(msc.descending_partitions, msc.max_hierarchy)
            elif kind == 'ascend':
                post.msc(msc.ascending_partitions, msc.min_hierarchy)
            else:
                post.msc(msc.base_partitions, msc.hierarchy)

            mc = post.build().verify().get_tree(measure)
            mc['type'] = kind
            mc['params'] = current
            regulus['morse']['complexes'][measure] = mc

        except RuntimeError as error:
            print(error)
