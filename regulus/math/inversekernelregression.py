from sklearn.kernel_ridge import KernelRidge
import numpy as np


def inversekernelregression(x, y, args=None):
    clf = KernelRidge(alpha=1.0, kernel='rbf')
    clf.fit(y.reshape(-1, 1), x)
    y_p = np.linspace(np.amin(y), np.amax(y), 100)
    x_p = clf.predict(y_p.reshape(-1, 1))

    model = {
        "inverse_kernel_reg": {
            'y': y_p.tolist(),
            'x': x_p.tolist()
        },

        'fitness': clf.score(y.reshape(-1, 1), x)
    }

    return model
