import ctypes
import numpy as np
from numba import jit, vectorize
from numba.extending import get_cython_function_address


_psi_address = get_cython_function_address(
    "scipy.special.cython_special", "__pyx_fuse_1psi"
)
_psi = ctypes.CFUNCTYPE(ctypes.c_double, ctypes.c_double, ctypes.c_int)(_psi_address)


@vectorize(["float64(float64)"])
def psi(X):
    # The second native argument bypasses Cython's Python dispatch.
    return _psi(X, 1)


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
