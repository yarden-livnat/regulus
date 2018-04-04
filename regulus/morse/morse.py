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
    dest = dict(src)
    for key, value in default.items():
        if key not in dest or dest[key] is None:
            dest[key] = default[key]
        print('merge', key, dest[key])
    return dest


def clean(params):
    for key, value in defaults.items():
        print('clean', key, params[key], defaults[key])
        if params[key] == value:
            print('remove', key)
            del params[key]
    return params


def morse(regulus, kind='smale', measures=None, args=None, debug=False):

    params = merge(args, defaults)

    ndims = len(regulus['dims'])
    if measures is None:
        measures = regulus['measures']

    pts = np.array(regulus['pts'])
    x = pts[:, 0:ndims]

    for i, measure in enumerate(measures):
        try:
            print('\npost ', measure)
            prev = rf.params(regulus, measure)
            current = merge(merge(args, prev), defaults)

            y = pts[:, ndims + i]
            msc = MSC(current['graph'], current['gradient'], current['knn'], current['beta'], current['norm'], aggregator='mean')  # connect=True
            msc.build(X=x, Y=y, names=regulus['dims'] + [measure])

            x = msc.X
            y = msc.Y
            post = Post(debug).data(y)

            if kind == 'descend':
                post.msc(msc.descending_partitions, msc.max_hierarchy)
            elif kind == 'ascend':
                post.msc(msc.ascending_partitions, msc.min_hierarchy)
            else:
                post.msc(msc.base_partitions, msc.hierarchy)

            mc = post.build().verify().get_tree(measure)
            mc['type'] = kind
            mc['params'] = clean(current)
            regulus['morse']['complexes'][measure] = mc

        except RuntimeError as error:
            print(error)
