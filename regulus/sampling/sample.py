import numpy as np
from numpy.random import default_rng
from scipy import stats


rng = default_rng()

def sample(curve, n, scale):
    x = curve['x']
    y = curve['y']
    sigma = curve['std']/2

    w = scale*sigma
    w /= w.sum()

    p = stats.rv_discrete(name='wp', values=(np.arange(len(y)), w))

    idx = p.rvs(size=n)
    sx = x[idx] + sigma[idx] * rng.uniform(-1, 1, n)
    sy = y[idx]

    return