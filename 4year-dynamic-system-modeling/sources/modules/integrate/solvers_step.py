import numpy as np
from numpy.typing import NDArray
from modules.systems.typing import RHSFunc
from numba import njit

# ================================================================================
@njit
def euler_step(
    df:         RHSFunc, 
    args:       NDArray[np.float64],
    h:          float,
    y:          NDArray[np.float64],
    y_next:     NDArray[np.float64],
) -> None:
    
    dy = np.zeros( 3, dtype=np.float64)
    
    df(y, args, dy)

    y_next[0] = y[0] + h * dy[0]
    y_next[1] = y[1] + h * dy[1]
    y_next[2] = y[2] + h * dy[2]

# ================================================================================
@njit
def runge_kutta_4_step(
    df:         RHSFunc, 
    args:       NDArray[np.float64],
    h:          float, 
    y:          NDArray[np.float64],
    y_next:     NDArray[np.float64]
) -> NDArray[np.float64]:

    dy = np.zeros( 3, dtype=np.float64 )
    k  = np.zeros( (4, 3), dtype=np.float64 )

    df(y, args, dy)
    k[0] = dy

    df(y + h * k[0] / 2, args, dy)
    k[1] = dy

    df(y + h * k[1] / 2, args, dy)
    k[2] = dy
    
    df(y + h * k[2], args, dy)
    k[3] = dy

    step = (h / 6) * (k[0] + 2*k[1] + 2*k[2] + k[3])    

    y_next[0] = y[0] + step[0]
    y_next[1] = y[1] + step[1]
    y_next[2] = y[2] + step[2]

# ================================================================================
@njit
def midpoint_step(
    df:         RHSFunc, 
    args:       NDArray[np.float64],
    h:          float, 
    y:          NDArray[np.float64],
    y_next:     NDArray[np.float64]
) -> NDArray[np.float64]:

    dy = np.zeros( 3, dtype=np.float64 )

    df(y, args, dy) # dy = k1
    y_mid = y + (h / 2) * dy
    df(y_mid, args, dy) # dy = k2
    
    y_next[0] = y[0] + h * dy
    y_next[1] = y[1] + h * dy
    y_next[2] = y[2] + h * dy

# ================================================================================
@njit
def euler_cromer_step(
    df:         RHSFunc, 
    args:       NDArray[np.float64],
    h:          float, 
    y:          NDArray[np.float64],
    y_next:     NDArray[np.float64]
) -> NDArray[np.float64]:
    
    dy = np.zeros( 3, dtype=np.float64 )

    y_next[:] = y[:] # save copy

    df(y_next, args, dy)
    y_next[0] = y[0] + h * dy[0]

    df(y_next, args, dy)
    y_next[1] = y[1] + h * dy[1]

    df(y_next, args, dy)
    y_next[2] = y[2] + h * dy[2]

# ================================================================================
@njit
def cd_step_lorenz(
    args:       NDArray[np.float64], 
    h:          float, 
    y:          NDArray[np.float64],
    y_next:     NDArray[np.float64]
) -> NDArray[np.float64]:
    
    sigma, rho, beta = args

    s = 0.5
    h1 = h * s
    h2 = h * (1 - s)

    denom_z = 1.0 + h2 * beta
    denom_y = 1.0 + h2
    denom_x = 1.0 + h2 * sigma

    sigma_h1 = sigma * h1
    sigma_h2 = sigma * h2

    x_i, y_i, z_i = y

    # Explicit half-step
    x_s = x_i + sigma_h1 * (y_i - x_i)
    y_s = y_i + h1 * (x_s * (rho - z_i) - y_i)
    z_s = z_i + h1 * (x_s * y_s - beta * z_i)

    # Implicit half-step (reverse order)
    z_nextt = (z_s + h2 * x_s * y_s) / denom_z
    y_nextt = (y_s + h2 * x_s * (rho - z_nextt)) / denom_y
    x_nextt = (x_s + sigma_h2 * y_nextt) / denom_x

    y_next[0] = x_nextt
    y_next[1] = y_nextt
    y_next[2] = z_nextt

    return y

# ================================================================================
@njit
def cd_step_chen(
    args:       NDArray[np.float64], 
    h:          float, 
    y:          NDArray[np.float64],
    y_next:     NDArray[np.float64]
):
    x0, y0, z0 = y
    a, b, c = args

    hh = h / 2

    # --- D1 ---
    x1 = (x0 + hh * a * y0) / (1 + hh * a)
    y1 = (y0 + hh * ((c - a) * x1 - x1 * z0)) / (1 - hh * c)
    z1 = (z0 + hh * x1 * y1) / (1 + hh * b)

    # --- D2 ---
    z2 = z1 + hh * (x1 * y1 - b * z1)
    y2 = y1 + hh * ((c - a) * x1 - x1 * z2 + c * y1)
    x2 = x1 + hh * a * (y2 - x1)

    y_next[0] = x2
    y_next[1] = y2
    y_next[2] = z2

# ================================================================================