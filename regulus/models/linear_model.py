from regulus.tree.traverse import *
from sklearn import linear_model as lm

MODEL_NAME = 'linear'


def linear_model(partition):
    model = lm.LinearRegression()
    model.fit(partition.x, partition.y)
    partition.models[MODEL_NAME] = model
