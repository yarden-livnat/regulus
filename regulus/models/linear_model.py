from sklearn import linear_model as lm

def linear_model(partition):
    model = lm.LinearRegression()
    model.fit(partition.x, partition.y)
    return model
