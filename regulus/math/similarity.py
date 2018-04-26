import numpy as np
from sklearn.kernel_ridge import KernelRidge

# should be able to calculate either parent or sibling similarity for selected method

# Synchronize vector length between two partitions

# Calculate Correlation between two vectors (normalize first then average between all dim?)

PTS_FOR_CORRELATION = 100


def update_regulus(regulus, spec, math_model=None):
    mscs = regulus['morse']['complexes']
    pts = np.array(regulus['pts'])
    dims = len(regulus["dims"])
    i = 0
    for measure, msc in mscs.items():  # in enumerate(mscs):
        try:
            print("Calculating " + spec + " correlation for " + measure)
            for partition in msc["partitions"]:
                target_partition = get_partition(partition, spec, msc["partitions"])
                calc_sim(partition, target_partition, msc['pts_idx'], pts, dims, i, spec)
        except Exception as e:
            print("Exception in correlation")
            print(e)
        i = i + 1


def get_partition(partition, spec, partitions):
    if spec == 'parent':
        return partitions[partition['parent']] if partition['parent'] is not None else None
    elif spec == 'sibling':
        parent = partitions[partition['parent']] if partition['parent'] is not None else None
        children_id = parent['children'] if parent is not None else None

        if children_id is not None:
            sibling_id = [id for id in children_id if id != partition['id']]
            return partitions[sibling_id[0]] if len(sibling_id) >= 1 else None
        else:
            return None


def calc_sim(p1, p2, idx, pts, ndims, measure_ind, spec):
    if 'model' not in p1:
        p1['model'] = {}

    if p2 is not None:
        # Extract pts from Partition 1
        span1 = p1["span"]
        pts_idx1 = idx[span1[0]:span1[1]]
        [min1, max1] = p1["minmax_idx"]
        pts_idx1.append(min1)
        pts_idx1.append(max1)

        data1 = pts[pts_idx1, :]
        x1 = data1[:, 0:ndims]
        y1 = data1[:, ndims + measure_ind]

        y1_min = pts[min1, ndims + measure_ind]
        y1_max = pts[max1, ndims + measure_ind]

        # Extract pts from Partition 2
        span2 = p2["span"]
        pts_idx2 = idx[span2[0]:span2[1]]
        [min2, max2] = p2["minmax_idx"]
        pts_idx2.append(min2)
        pts_idx2.append(max2)

        data2 = pts[pts_idx2, :]
        x2 = data2[:, 0:ndims]
        y2 = data2[:, ndims + measure_ind]

        y2_min = pts[min2, ndims + measure_ind]
        y2_max = pts[max2, ndims + measure_ind]

        # Calculate Union range
        y_min = y2_min if y2_min < y1_min else y1_min
        y_max = y2_max if y2_max > y1_max else y1_max

        y_p = np.linspace(y_min, y_max, PTS_FOR_CORRELATION)

        # Predict Xs with Predictor for P1
        clf1 = KernelRidge(alpha=1.0, kernel='rbf')
        clf1.fit(y1.reshape(-1, 1), x1)
        x_p1 = clf1.predict(y_p.reshape(-1, 1))

        # Predict Xs with Predictor for P2

        clf2 = KernelRidge(alpha=1.0, kernel='rbf')
        clf2.fit(y2.reshape(-1, 1), x2)
        x_p2 = clf2.predict(y_p.reshape(-1, 1))

        # order?
        corre = np.corrcoef(x_p1.T, x_p2.T)
        # print(x_p1.T)
        # print(corre)

        total = 0
        n_features = int(corre.shape[0] / 2)

        for i in range(n_features):
            total = total + corre[i, i + n_features]

        p1['model'][spec + "_correlation"] = None if np.isnan(total) else total / n_features

        # dist = cdist(x_p1, x_p2, 'mahalanobis', VI=None)

        # p1['model'][spec + "_correlation"] = dist
        # if np.isnan(corre[0][1]):
        #    p1['model'][spec + "_correlation"] = None

    else:
        p1['model'][spec + "_correlation"] = None


class Similarity(object):
    def factory(type):
        if type == "parent":
            return Parent()
        elif type == "sibling":
            return Sibling()
        raise AssertionError("Bad Sampling Method: " + type)

    factory = staticmethod(factory)


class Parent(Similarity):

    def compute(self, regulus):
        update_regulus(regulus, 'parent')


class Sibling(Similarity):
    def compute(self, regulus):
        update_regulus(regulus, 'sibling')
