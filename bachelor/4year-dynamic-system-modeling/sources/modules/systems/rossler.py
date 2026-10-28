import numpy as np
from numpy.typing import NDArray
from numba import njit

@njit
def rossler(
    state:  NDArray[np.float64], 
    args:   NDArray[np.float64],
    out:    NDArray[np.float64]
) -> None:
    x, y, z = state
    a, b, c = args

    out[0] = -y - z
    out[1] = x + a * y
    out[2] = b + z * (x - c)