from sklearn import linear_model as lm

def linear_model(partition):
    # print('new model for', partition.id)
    model = lm.LinearRegression()
    model.fit(partition.x, partition.y)
    return model
