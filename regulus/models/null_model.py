class NullModel(object):
    def __init__(self):
        self.coef_ = []
        self.intercept_ = 0
        pass

    def fit(self, x, y):
        pass

    def score(self, x, y):
        return 0

    def predict(self, x):
        return x
