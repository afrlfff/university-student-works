import numpy as np
from numpy.typing import NDArray
from numba import njit

@njit
def chen(
    state:  NDArray[np.float64], 
    args:   NDArray[np.float64],
    out:    NDArray[np.float64]
) -> None:
    x, y, z = state
    a, b, c = args

    out[0] = a*(y - x)              # dx
    out[1] = (c - a)*x - x*z + c*y  # dy
    out[2] = x*y - b*z              # dz