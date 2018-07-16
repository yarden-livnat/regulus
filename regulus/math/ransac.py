from sklearn import linear_model


def ransac(x, y, args=None):
    ransac = linear_model.RANSACRegressor()
    ransac.fit(x, y)

    model = {
        "reg": {
            "coeff": ransac.coef_.tolist(),
            "intercept": ransac.intercept_
        },

        'fitness': ransac.score(x, y)
    }

    return model
