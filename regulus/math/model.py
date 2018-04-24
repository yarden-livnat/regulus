import numpy as np
from regulus.math.linear_reg import linear_reg
from regulus.math.pca import pca
from regulus.math.inv_kernel_reg import inv_kernel_reg

MODELS = {
    'linear_reg': {
        'method': linear_reg,
        'args': None
    },
    'pca': {
        'method': pca,
        'args': 2
    }
    # ,
    # inv_kernel_reg': {
    #    'method': inv_kernel_reg,
    #    'args': None
    # }
}


def update_regulus(regulus, spec):
    mscs = regulus['morse']['complexes']
    pts = np.array(regulus['pts'])
    dims = len(regulus["dims"])
    i = 0
    for name, msc in mscs.items():  # in enumerate(mscs):
        print("Calculating Model " + spec + " for " + name)
        update_msc(msc, pts, dims, i, spec)
        i = i + 1


def update_msc(msc, pts, ndims, measure_ind, spec):
    try:
        for partition in msc["partitions"]:
            update_partition(partition, msc['pts_idx'], pts, ndims, measure_ind, spec)
    except Exception as e:
        print('Exception in model')
        print(e)


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

    model_key = list(model.keys())[0]

    if 'model' not in partition:
        partition['model'] = {}

    partition['model'][model_key] = model[model_key]


def compute_model(x, y, spec):
    model = {}
    method = MODELS[spec]['method']
    args = MODELS[spec]['args']

    model[spec] = method(x, y, args)

    return model


class Model(object):
    def factory(type):
        if type == "linear":
            return Linear()
        elif type == "pca":
            return Pca()
        raise AssertionError("Unknown Model: " + type)

    factory = staticmethod(factory)


class Pca(Model):

    def compute(self, regulus):
        update_regulus(regulus, 'pca')


class Linear(Model):
    def compute(self, regulus):
        update_regulus(regulus, 'linear_reg')
