import numpy as np
from numpy.typing import NDArray
from numba import njit

@njit
def lorenz(
    state:  NDArray[np.float64], 
    args:   NDArray[np.float64],
    out:    NDArray[np.float64]
) -> None:
    x, y, z = state
    sigma, rho, beta = args

    out[0] = sigma * (y - x)        # dx
    out[1] = x * (rho - z) - y      # dy
    out[2] = x*y - beta*z           # dz