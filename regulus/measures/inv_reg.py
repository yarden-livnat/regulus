import numpy as np
import pandas as pd

TAU = 0.1
N = 20


def radial_kernel(x0, X, tau):
    return np.exp(np.sum((X - x0) ** 2, axis=1) / (-2 * tau * tau))


def lowess(X, Y, tau):
    # add bias term
    X = np.c_[np.ones(len(X)), X]

    def f(x):
        x = np.r_[1, x]
        # fit model: normal equations with kernel
        xw = X.T * radial_kernel(x, X, tau)
        beta = np.linalg.pinv(xw @ X) @ xw @ Y
        # predict value
        return x @ beta
    return f


def sample_lowess(S, X, Y, tau=TAU):
    f = lowess(X, Y, tau)
    return np.array([f(s) for s in S])


def inverse_lowess(X, Y, n=N, tau=TAU):
    S = np.linspace(np.amin(Y), np.amax(Y), n)
    return sample_lowess(S, Y, X, tau)


def inverse_lowess_std(X, Y, n=N, tau=TAU):
    rho = (sample_lowess(Y, Y, X, tau) - X) ** 2

    Y1 = np.c_[np.ones(len(Y)), Y]
    S = np.linspace(np.amin(Y), np.amax(Y), n)
    S1 = np.c_[np.ones(len(S)), S]
    W = np.array([radial_kernel(s, Y1, tau) for s in S1])
    denom = np.sum(W, axis=1)

    wr = W @ rho
    std = np.c_[[wr[c]/denom for c in list(wr)]]
    return std.T


def inverse_regression(context, node):
    partition = node.data
    if partition.y.size < 2:
        return []

    X = partition.x
    Y = partition.y
    S = np.linspace(np.amin(Y), np.amax(Y), N)
    line = sample_lowess(S, Y, X)
    std = inverse_lowess_std(X, Y)
    return {'x': pd.DataFrame(line, columns=list(X)), 'y': S, 'std': pd.DataFrame(std, columns=list(X))}


def inverse_regression_scale(context, node):
    d = context['inverse_regression'][node]
    s = node.regulus.pts.scaler
    return {'x': s.inverse_transform(d['x'], copy=True),
            'y': d['y'],
            'std': s.inverse_transform(d['std'], copy=True)
            }