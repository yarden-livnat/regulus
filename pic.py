import sys
import csv
import numpy as np
import pickle
from sklearn import linear_model
from sklearn.kernel_ridge import KernelRidge


class Regulus(object):
    def __init__(self, pts, header, dims, measure):
        self.pts = pts
        self.header = header
        self.dims = dims
        self.measure = self.dims + measure
        self.models = {}

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def fwd(self):
        model = linear_model.LinearRegression()
        model.fit(self.pts[:, 0:self.dims], self.pts[:, self.measure])
        self.models['linear_reg'] = model

    def inv(self):
        x = self.pts[:, 0:self.dims]
        y = self.pts[:, self.measure]
        model = KernelRidge(alpha=1.0, kernel='rbf')
        model.fit(y.reshape(-1, 1), x)
        self.models['inv_reg'] = model


def run(filename, d, measure):
    with open(filename) as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [[float(x) for x in row] for row in reader]
    pts = np.array(data)

    r = Regulus(pts, header, d, measure)
    r.save('r.p')
    r.fwd()
    r.save('r_fwd.p')
    r.inv()
    r.save('r_inv.p')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1], 6, 3)
    else:
        print('usageL count filename')