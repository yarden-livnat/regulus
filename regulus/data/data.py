import pandas as pd
from sklearn.preprocessing import StandardScaler


class Data(object):
    def __init__(self, x, values, measure=None):
        self.x = pd.DataFrame(x)
        self.values = pd.DataFrame(values)
        self.y = None
        self.measure = None
        self.scaler = None

        if measure is None:
            measure = list(self.values.columns)[-1]

        self.pivot(measure)

    @staticmethod
    def read_csv(filename, ndims=None, measure=None):
        return Data.from_pts(pd.read_csv(filename), ndims=ndims, measure=measure)

    @staticmethod
    def from_pts(pts, cols=None, ndims=None, measure=None):
        pts = pd.DataFrame(pts, columns=cols)
        if ndims is None:
            ndims = pts.shape[1]-1
        cols = list(pts.columns)
        x = pts.loc[:, cols[:ndims]]
        values = pts.loc[:, cols[ndims:]]
        return Data(x, values, measure)

    def normalize(self, scaler=None):
        if scaler is None:
            scaler = StandardScaler(copy=False)
        self.scaler = scaler
        self.scaler.fit_transform(self.x)

    def pivot(self, measure):
        self.measure = measure
        self.y = self.values.loc[:, measure]
