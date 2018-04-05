from sklearn import linear_model


def linearregression(x, y, args=None):
    reg = linear_model.LinearRegression()
    reg.fit(x, y)

    model = {
        "linear_reg": {
            "coeff": reg.coef_.tolist(),
            "intercept": reg.intercept_
        },

        'fitness': reg.score(x, y)
    }

    return model
