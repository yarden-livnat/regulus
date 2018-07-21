import numpy as np
# from regulus.math.linear_reg import linear_reg
# from regulus.math.pca import pca
# from regulus.math.inv_kernel_reg import inv_kernel_reg
from regulus.models.linear_reg import LinearReg
from regulus.measures.fwd_fitness import fwd_fitness
from regulus.measures.parent_similarity import parent_similarity


default_models = {
    'linear_reg': LinearReg
}

default_attrs = {
    'fitness': fwd_fitness,
    'parent_similarity': parent_similarity
}

data = dict()


def get_pts(partition, idx, pts):
    id = partition['id']
    if id not in data:
        span = partition["span"]
        pts_idx = idx[span[0]:span[1]]
        [min_idx, max_idx] = partition["minmax_idx"]
        if min_idx not in pts_idx:
            pts_idx.append(min_idx)
        if max_idx not in pts_idx:
            pts_idx.append(max_idx)
        data[id] = pts[pts_idx, :]
    return data[id]


def update_regulus(regulus, spec):
    mscs = regulus['morse']['complexes']
    pts = np.array(regulus['pts'])
    dims = len(regulus["dims"])

    for name, msc in mscs.items():
        i = regulus['measures'].index(name)
        update_msc(msc, pts, dims, i, spec)


def update_msc(msc, pts, ndims, measure_idx, spec):
    global data
    try:
        data = dict()
        idx = msc['pts_idx']
        partitions = msc["partitions"]
        for partition in partitions:
            compute_models(partition, idx, pts, ndims, measure_idx, spec)

        for partition in partitions:
            compute_attrs(msc, partition, idx, pts, ndims, measure_idx, spec)

        for partition in partitions:
            models = partition['models']
            for name, model in models.items():
                if not isinstance(model, dict):
                    models[name] = model.desc()
    except Exception as e:
        print(e)   # todo: what exception is the try protecting?


def compute_models(partition, idx, pts, ndims, measure_ind, spec):
    np_pts = get_pts(partition, idx, pts)
    x = np_pts[:, 0:ndims]
    y = np_pts[:, ndims + measure_ind]

    if 'models' not in partition:
        partition['models'] = dict()
    for name, model in spec['models'].items():
        partition['models'][name] = model(x, y)


def compute_attrs(msc, partition, idx, pts, ndims, measure_ind, spec):
    np_pts = get_pts(partition, idx, pts)
    x = np_pts[:, 0:ndims]
    y = np_pts[:, ndims + measure_ind]

    if 'attrs' not in partition:
        partition['attrs'] = dict()
    for name, f in spec['attrs'].items():
        partition['attrs'][name] = f(msc, partition, x, y)


def update(regulus, spec=None):
    if spec is None:
        spec = {}
    if 'models' not in spec:
        spec['models'] = default_models
    if 'attrs' not in spec:
        spec['attrs'] = default_attrs
    update_regulus(regulus, spec)


