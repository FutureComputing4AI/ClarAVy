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
