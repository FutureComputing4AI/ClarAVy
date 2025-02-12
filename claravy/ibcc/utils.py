import numba
import numpy as np
from numba import jit

@jit(nopython=True)
def unique(X):
    """Reimplementation of np.unique() so that it works with numba JIT."""
    b = np.sort(X)
    unique = list(b[:1])
    counts = [1 for _ in unique]
    for x in b[1:]:
        if x != unique[-1]:
            unique.append(x)
            counts.append(1)
        else:
            counts[-1] += 1
    return unique, counts


# From https://gist.github.com/timvieira/656d9c74ac5f82f596921aa20ecb6cc8
@numba.vectorize
def psi(x):
    """Fast approximation of the digamma function. Assumes x > 0."""
    if x < 0:
        raise ValueError("digamma input must be greater than 0")
    r = 0
    while(x <= 5):
        r = r - (1 / x)
        x += 1
    f = (x * x)
    f = 1 / f
    t = f * (-1/12.0 + f * (1/120.0 + f * (-1/252.0 + f * (1/240.0 + f * (-1 / 132.0 + f * (691/32760.0 + f * (-1/12.0 + f * 3617/8160.0)))))))
    return r + np.log(x) - 0.5 / x + t
