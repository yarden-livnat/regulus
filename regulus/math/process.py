import numpy as np
from regulus.math.linearregression import linearregression
from regulus.math.pca import pca
from regulus.math.inversekernelregression import inversekernelregression

defaults = {
    'linear_reg': {
        'method': linearregression,
        'args': None
    },
    'pca': {
        'method': pca,
        'args': 2
    },
    'inverse_kernel_regression': {
        'method': inversekernelregression,
        'args': None
    }
}


def update_regulus(regulus, spec):
    mscs = regulus['morse']['complexes']
    pts = np.array(regulus['pts'])
    dims = len(regulus["dims"])
    i = 0
    for measure, msc in mscs.items():  # in enumerate(mscs):
        update_msc(msc, pts, dims, i, spec)
        i = i + 1


def update_msc(msc, pts, ndims, measure_ind, spec):
    if 'pts_idx' not in msc:
        print('ignored')
    for partition in msc["partitions"]:
        update_partition(partition, msc['pts_idx'], pts, ndims, measure_ind, spec)


def update_partition(partition, idx, pts, ndims, measure_ind, spec):
    span = partition["span"]
    pts_idx = idx[span[0]:span[1]]
    [min, max] = partition["minmax_idx"]
    pts_idx.append(min)
    pts_idx.append(max)

    data = pts[pts_idx, :]
    x = data[:, 0:ndims]
    y = data[:, ndims + measure_ind]

    model = compute_model(x, y, spec)

    partition['model'] = model


def compute_model(x, y, spec):
    model = {}

    for method in spec.keys():
        cur_method = spec[method]['method']
        args = spec[method]['args']
        model[method] = cur_method(x, y, args)

    return model


def process(regulus, spec=None):
    if spec is None:
        spec = defaults

    update_regulus(regulus, spec)
