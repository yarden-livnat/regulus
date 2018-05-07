from sklearn.kernel_ridge import KernelRidge
import time
import numpy as np

import abc
import six


@six.add_metaclass(abc.ABCMeta)
class Model(object):
    @abc.abstractmethod
    def model(self, v1, v2):
        pass


class Inv_reg(object):
    def model(self, x1, y1):
        clf = KernelRidge(alpha=1.0, kernel='rbf')
        clf.fit(y1.reshape(-1, 1), x1)
        return clf


class Linear_reg(object):
    def model(self, v1, v2):
        print(v1, v2)


MODEL_FUNCS = {
    "inv_reg": Inv_reg,
    "linear_reg": Linear_reg
}


def create_models(regulus, model=None):
    # if model is None:
    #    model = calc_inverse


    # register model
    if model is None:
        Model.register(Inv_reg)
        new_model = Inv_reg()

    elif model in MODEL_FUNCS:
        model_func = MODEL_FUNCS(model)
        Model.register(model_func)
        new_model = model_func()
    else:
        print("Could not recognize similarity functions")
        return

    cur_model = new_model.model


    # Compute models for all partitions
    print("Calculating inverse regression: ")
    model_dict = {}
    mscs = regulus['morse']['complexes']
    pts = np.array(regulus['pts'])
    measure_ind = 0
    ndims = len(regulus["dims"])
    for measure, msc in mscs.items():

        start_CPU = time.clock()

        # print("Measure = {}".format(measure))
        # print("Total Partitions = {}".format(len(msc['partitions'])))

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

            clf = cur_model(x1, y1)

            cur_measure[id] = clf

            end = time.clock()

            if span1[1] - span1[0] > 2000:
                print("Fit regression model: %f seconds" % (end - start) + " for %i points" % (
                        span1[1] - span1[0]))

        measure_ind = measure_ind + 1

        end_CPU = time.clock()

        print("Time to compute regression model: %f seconds" % (end_CPU - start_CPU) + " for {}".format(
            len(msc['partitions'])) + " partitions for measure {}".format(measure))
    return model_dict


'''
def calc_inverse(x1, y1):
    clf = KernelRidge(alpha=1.0, kernel='rbf')
    clf.fit(y1.reshape(-1, 1), x1)
    return clf

'''
