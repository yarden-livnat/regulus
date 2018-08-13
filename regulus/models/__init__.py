from .linear_model import *

class NullModel(object):
    def __init__(self):
        pass

    def fit(self, x, y):
        pass

    def score(self, x, y):
        return 0;

    def predict(self, x):
        return x

def null_model(_):
    return NullModel()
