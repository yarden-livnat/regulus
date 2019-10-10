import math
import numpy as np
import pandas as pd

SIGMA = 0.1
N = 40


def radial_kernel(x0, X, sigma):
    return np.exp(np.sum((X - x0) ** 2, axis=1) / (-2 * sigma * sigma))


def gaussian(sigma):
    f = 1 / (math.sqrt(2*math.pi) * sigma)

    def kernel(x, X):
        return f * np.exp(np.sum((X - x) ** 2, axis=1) / (-2 * sigma * sigma))
    return kernel


GAUSSIAN = gaussian(SIGMA)


def lowess(X, Y, kernel=GAUSSIAN):
    # add bias term
    X = np.c_[np.ones(len(X)), X]

    def f(x):
        x = np.r_[1, x]
        # fit model: normal equations with kernel
        xw = X.T * kernel(x, X)
        beta = np.linalg.pinv(xw @ X) @ xw @ Y
        # predict value
        return x @ beta
    return f


def sample_lowess(S, X, Y, kernel=GAUSSIAN):
    f = lowess(X, Y, kernel)
    return np.array([f(s) for s in S])


def inverse_lowess(X, Y, S=None, n=N, kernel=GAUSSIAN):
    if S is None:
        S = np.linspace(np.amin(Y), np.amax(Y), n)
    return sample_lowess(S, Y, X, kernel)


def inverse_lowess_std(X, Y, n=N, kernel=GAUSSIAN):
    Y1 = np.c_[np.ones(len(Y)), Y]
    S = np.linspace(np.amin(Y), np.amax(Y), n)
    S1 = np.c_[np.ones(len(S)), S]
    W = np.array([kernel(s, Y1) for s in S1])
    denom = np.sum(W, axis=1)

    rho = (inverse_lowess(X, Y, S=Y, kernel=kernel) - X) ** 2
    wr = W @ rho
    std = np.c_[[wr[c]/denom for c in list(wr)]]
    return std.T


def inverse(X, Y, kernel=GAUSSIAN, scaler=None):
    S = np.linspace(np.amin(Y), np.amax(Y), N)
    line = sample_lowess(S, Y, X, kernel)
    std = inverse_lowess_std(X, Y, kernel=kernel)

    if scaler is not None:
        line = scaler.inverse_transform(line)
        std = std * scaler.scale_
    return S, line, std


def inverse_regression(kernel=GAUSSIAN, scale=True):
    def f(context, node):
        partition = node.data
        if partition.y.size < 2:
            return []

        scaler = node.regulus.pts.scaler if scale else None
        S, line, std = inverse(partition.x, partition.y, kernel, scaler)
        return [dict(x=line[:, c], y=S, std=std[:, c]) for c in range(partition.x.shape[1])]
    return f
