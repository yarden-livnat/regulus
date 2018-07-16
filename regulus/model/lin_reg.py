from sklearn import linear_model

class LinReg(object):
    def __init__(self, x=None, y=None):
        self.model = linear_model.LinearRegression()
        if x is not None and y is not None:
            self.fit(x,y)

    def fit(self, x, y):
        self.model.fit(x, y)

    def score(self, x, y):
        return self.model.score(x, y)
