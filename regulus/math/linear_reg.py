from sklearn import linear_model


def linear_reg(x, y, args=None):
    reg = linear_model.LinearRegression()
    reg.fit(x, y)

    model = {
        "reg": {
            "coeff": reg.coef_.tolist(),
            "intercept": reg.intercept_
        },

        'fitness': reg.score(x, y)
    }

    return model
