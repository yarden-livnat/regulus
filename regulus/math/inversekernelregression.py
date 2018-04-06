from sklearn.kernel_ridge import KernelRidge


def inversekernelregression(x, y, args=None):
    clf = KernelRidge(alpha=1.0, kernel='rbf')
    clf.fit(y.reshape(-1, 1), x)

    model = {
        "inverse_kernel_reg": {
            "weight_vec": clf.dual_coef_.tolist(),
            "training_data": clf.X_fit_.tolist()
        },

        'fitness': clf.score(y.reshape(-1,1),x)
    }

    return model
