import pandas as pd
from sklearn.preprocessing import StandardScaler


class Data(object):
    def __init__(self, x, values):
        self.x = pd.DataFrame(x)
        self.values = pd.DataFrame(values)
        self.scaler = None

    @staticmethod
    def read_csv(filename, ndims=None):
        return Data.from_df(pd.read_csv(filename), ndims=ndims)

    @staticmethod
    def from_pts(pts, cols=None, ndims=None):
        pts = pd.DataFrame(pts, columns=cols)
        if ndims is None:
            ndims = pts.shape[1]-1
        cols = list(pts.columns)
        x = pts.loc[:, cols[:ndims]]
        values = pts.loc[:, cols[ndims:]]
        return Data(x, values)

    @staticmethod
    def from_df(pts, ndims=None):
        if ndims is None:
            ndims = pts.shape[1] - 1
        cols = list(pts.columns)
        x = pts.loc[:, cols[:ndims]]
        values = pts.loc[:, cols[ndims:]]
        return Data(x, values)

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

    def inverse(self, x):
        return x if self.scaler is None else pd.DataFrame(self.scaler.inverse_transform(x, copy=True), columns=x.columns)

    def y(self, measure):
        return self.values.loc[:, measure]
