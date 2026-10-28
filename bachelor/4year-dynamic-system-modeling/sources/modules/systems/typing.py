import numpy as np
from numpy.typing import NDArray
from typing import Callable

# RHSFunc - Right-hand size function - function that calculated the the right side of ODE equation
# (like dy/dt = f(t, y, out))

RHSFunc = Callable[
    [NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]], None
]