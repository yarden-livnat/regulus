import numpy as np
from sklearn.kernel_ridge import KernelRidge
import time

# should be able to calculate either parent or sibling similarity for selected method

# Synchronize vector length between two partitions

# Calculate Correlation between two vectors (normalize first then average between all dim?)

PTS_FOR_CORRELATION = 50


def create_models(regulus):
    print("Calculating inverse regression: ")
    model_dict = {}
    mscs = regulus['morse']['complexes']
    pts = np.array(regulus['pts'])
    measure_ind = 0
    ndims = len(regulus["dims"])
    for measure, msc in mscs.items():

        start_CPU = time.clock()

        print("Measure = {}".format(measure))
        print("Total Partitions = {}".format(len(msc['partitions'])))

        model_dict[measure] = {}
        cur_measure = model_dict[measure]
        for partition in msc['partitions']:

            start = time.clock()

            span1 = partition["span"]
            idx = msc['pts_idx']
            id = partition['id']
            pts_idx1 = idx[span1[0]:span1[1]]
            [min1, max1] = partition["minmax_idx"]
            pts_idx1.append(min1)
            pts_idx1.append(max1)

            data1 = pts[pts_idx1, :]

            x1 = data1[:, 0:ndims]
            y1 = data1[:, ndims + measure_ind]

            clf = KernelRidge(alpha=1.0, kernel='rbf')
            clf.fit(y1.reshape(-1, 1), x1)
            cur_measure[id] = clf

            end = time.clock()

            if span1[1]-span1[0] > 2000:
                print("Time to compute regression model: %f seconds" % (end - start) + " for %i points" %(span1[1]-span1[0]))

        measure_ind = measure_ind + 1

        end_CPU = time.clock()

        print("Time to compute regression model: %f seconds" % (end_CPU - start_CPU))
    return model_dict


def update_regulus(regulus, specs, math_model, sim_func = None):
    for spec in specs:
        mscs = regulus['morse']['complexes']
        # pts = np.array(regulus['pts'])
        # dims = len(regulus["dims"])
        i = 0

        for measure, msc in mscs.items():  # in enumerate(mscs):
            try:
                start_CPU = time.clock()

                print("Calculating " + spec + " correlation for " + measure)
                for partition in msc["partitions"]:

                    cur_idx = partition["id"]
                    target_partition = get_partition(partition, spec, msc["partitions"])
                    if target_partition is not None:

                        target_idx = target_partition["id"]
                        # only calculate sim once between every pair
                        if spec is 'parent' or (spec is 'sibling' and int(cur_idx) < int(target_idx)):
                            # print([cur_idx, target_idx])

                            # Compute Similarity
                            sim = comp_sim(cur_idx, target_idx, regulus, measure, math_model, sim_func)
                            # Set Similarity
                            set_sim(cur_idx, target_idx, regulus, measure, spec, sim)

                    else:
                        set_sim(cur_idx, None, regulus, measure, spec, None)

                end_CPU = time.clock()

                print("Time to calculate ".format(spec)+" similarity for ".format(measure) + ": %f seconds" % (end_CPU - start_CPU))

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


'''
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
        start_CPU = time.clock()

        clf1 = KernelRidge(alpha=1.0, kernel='rbf')
        clf1.fit(y1.reshape(-1, 1), x1)

        print(clf1)

        end_CPU = time.clock()
        print("F1 fit: %f CPU seconds" % (end_CPU - start_CPU))

        start_CPU = time.clock()

        x_p1 = clf1.predict(y_p.reshape(-1, 1))

        end_CPU = time.clock()
        print("F1 predict: %f CPU seconds" % (end_CPU - start_CPU))

        # Predict Xs with Predictor for P2

        clf2 = KernelRidge(alpha=1.0, kernel='rbf')

        start_CPU = time.clock()

        clf2.fit(y2.reshape(-1, 1), x2)

        end_CPU = time.clock()

        print("F2 fit: %f CPU seconds" % (end_CPU - start_CPU))

        start_CPU = time.clock()

        x_p2 = clf2.predict(y_p.reshape(-1, 1))

        end_CPU = time.clock()

        print("F2 predict: %f CPU seconds" % (end_CPU - start_CPU))

        # order?

        start_CPU = time.clock()

        corre = np.corrcoef(x_p1.T, x_p2.T)

        end_CPU = time.clock()

        print("Correlation: %f CPU seconds" % (end_CPU - start_CPU))
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
'''

# Compute Similarity with specified sim_function

def comp_sim(id1, id2, regulus, measure, model_dict, sim_func=None):
    mscs = regulus['morse']['complexes']
    msc = mscs[measure]
    idx = msc['pts_idx']
    pts = np.array(regulus['pts'])
    ndims = len(regulus["dims"])
    measures = regulus['measures']
    measure_ind = measures.index(measure)
    partitions = msc['partitions']
    p1 = partitions[int(id1)]
    p2 = partitions[int(id2)]

    if sim_func is None:
        sim_func = default_sim
    [y_min, y_max] = get_union_range(p1, p2, pts, ndims, measure_ind, idx)

    y_p = np.linspace(y_min, y_max, PTS_FOR_CORRELATION)

    model1 = model_dict[measure][id1]
    model2 = model_dict[measure][id2]

    x_p1 = model1.predict(y_p.reshape(-1, 1))
    x_p2 = model2.predict(y_p.reshape(-1, 1))

    x_p1_T = x_p1.T
    x_p2_T = x_p2.T

    nfeatures = len(x_p1_T)

    total_sim = 0
    for i in range(nfeatures):
        total_sim = total_sim + sim_func(x_p1_T[i, :], x_p2_T[i, :])

    return None if np.isnan(total_sim) else total_sim / nfeatures


def set_sim(id1, id2, regulus, measure, sim_type, sim):
    mscs = regulus['morse']['complexes']
    msc = mscs[measure]

    partitions = msc['partitions']

    p1 = partitions[int(id1)]

    if sim_type is 'parent' or id2 is None:
        p1['model'][sim_type + "_correlation"] = sim

    else:
        p2 = partitions[int(id2)]
        if int(id1) < int(id2):
            p1['model'][sim_type + "_correlation"] = sim
            p2['model'][sim_type + "_correlation"] = sim


def get_union_range(p1, p2, pts, ndims, measure_ind, idx):
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
    return [y_min, y_max]


def default_sim(v1, v2):
    from scipy.stats.stats import pearsonr
    r, p = pearsonr(v1, v2)
    return r


def calc_similarity(regulus, types, sim_func = None):

    model = create_models(regulus)

    start_CPU = time.clock()

    update_regulus(regulus, types, model, sim_func)

    end_CPU = time.clock()

    print("Calculate Similarity with Models: %f seconds" % (end_CPU - start_CPU))


'''
class Similarity(object):
    def factory(type):
        if type == "parent":
            return Parent()
        elif type == "sibling":
            return Sibling()
        raise AssertionError("Bad Sampling Method: " + type)

    factory = staticmethod(factory)


class Parent(Similarity):

    def compute(self, regulus, types):

        start_CPU = time.clock()

        model = create_models(regulus)

        end_CPU = time.clock()

        print("Calculate All Models: %f seconds" % (end_CPU - start_CPU))

        start_CPU = time.clock()

        update_regulus(regulus, types, model)

        end_CPU = time.clock()

        print("Calculate Similarity with Models: %f seconds" % (end_CPU - start_CPU))


class Sibling(Similarity):
    def compute(self, regulus):
        update_regulus(regulus, 'sibling')

'''
