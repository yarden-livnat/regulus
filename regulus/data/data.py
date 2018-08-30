import pandas as pd
from sklearn.preprocessing import StandardScaler


class Data(object):
    def __init__(self, x, values, measure=None):
        self.x = pd.DataFrame(x)
        self.values = pd.DataFrame(values)
        self.scaler = None

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


    def normalize(self, scaler=None, copy=False):
        if scaler is None:
            scaler = StandardScaler(copy=copy)
        self.scaler = scaler
        self.x = pd.DataFrame(self.scaler.fit_transform(self.x), columns=self.x.columns)

    def size(self):
        return len(self.values)

    @property
    def original_x(self):
        return self.x if self.scaler is None else pd.DataFrame(self.scaler.inverse_transform(self.x, copy=True), columns=self.x.columns)


    def y(self, measure):
        return self.values.loc[:, measure]
