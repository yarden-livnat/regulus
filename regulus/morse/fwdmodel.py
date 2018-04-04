import numpy as np
from sklearn import linear_model

import regulus.file as rf


def update_partition(partition, idx, pts, ndims, measure):
    span = partition["span"]
    pts_idx = idx[span[0]:span[1]]
    [min, max] = partition["minmax_idx"]
    pts_idx.append(min)
    pts_idx.append(max)

    data = pts[pts_idx, :]
    x = data[:, 0:ndims]
    y = data[:, ndims + measure]

    reg = linear_model.LinearRegression()
    reg.fit(x, y)

    partition['model'] = {
        "linear_reg": {
            "coeff": reg.coef_.tolist(),
            "intercept": reg.intercept_
            },

        'fitness': reg.score(x,y)
        }


def update_msc(msc, pts, ndims, measure):
    print(msc['name'])
    if 'pts_idx' not in msc:
        print('ignored')
    for partition in msc["partitions"]:
        update_partition(partition, msc['pts_idx'], pts, ndims, measure)


def calc_regression(mscs, pts, ndims):
    array_pts = np.array(pts)
    for measure, msc in enumerate(mscs):
        update_msc(msc, array_pts, ndims, measure)


if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser(description='computer linear fwd model')
    p.add_argument('filename', help='regulus json file')
    p.add_argument('-o', '--out', help='output file')
    ns = p.parse_args()

    regulus= rf.load(ns.filename)
    calc_regression(regulus["mscs"], regulus["pts"], len(regulus["dims"]))

    rf.save(regulus, ns.out)