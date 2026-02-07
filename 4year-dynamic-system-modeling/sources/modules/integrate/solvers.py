import numpy as np
from numpy.typing import NDArray
from modules.systems.typing import RHSFunc
from numba import njit

# ================================================================================
@njit
def euler(
    df:         RHSFunc, 
    args:       NDArray[np.float64],
    n_steps:    float, 
    h:          float, 
    y0:         NDArray[np.float64]
) -> NDArray[np.float64]:
    
    y   = np.zeros( (n_steps, len(y0)), dtype=np.float64 )
    dy  = np.zeros( len(y0), dtype=np.float64 )

    y[0] = y0
    for i in range(1, n_steps):
        df(y[i-1], args, dy)
        y[i] = y[i-1] + h * dy
    
    return y

# ================================================================================
@njit
def runge_kutta_4(
    df:         RHSFunc, 
    args:       NDArray[np.float64], 
    n_steps:    float, 
    h:          float, 
    y0:         NDArray[np.float64]
) -> NDArray[np.float64]:

    y   = np.zeros( (n_steps, len(y0)), dtype=np.float64 )
    dy  = np.zeros( len(y0), dtype=np.float64 )
    k   = np.zeros( (4, len(y0)), dtype=np.float64 )
    
    y[0] = y0
    for i in range(1, n_steps):
        df(y[i-1], args, dy)
        k[0] = dy

        df(y[i-1] + h * k[0] / 2, args, dy)
        k[1] = dy

        df(y[i-1] + h * k[1] / 2, args, dy)
        k[2] = dy
        
        df(y[i-1] + h * k[2], args, dy)
        k[3] = dy

        y[i] = y[i-1] + (h / 6) * (k[0] + 2*k[1] + 2*k[2] + k[3])
    
    return y

# ================================================================================
@njit
def midpoint(
    df:         RHSFunc, 
    args:       NDArray[np.float64], 
    n_steps:    float, 
    h:          float, 
    y0:         NDArray[np.float64]
) -> NDArray[np.float64]:
    
    y = np.zeros( (n_steps, len(y0)), dtype=np.float64 )
    dy = np.zeros( len(y0), dtype=np.float64 )

    y[0] = y0

    for i in range(1, n_steps):
        y_prev = y[i-1]

        df(y_prev, args, dy) # dy = k1
        y_mid = y_prev + (h / 2) * dy
        
        df(y_mid, args, dy) # dy = k2
        y[i] = y_prev + h * dy

    return y

# ================================================================================
@njit
def euler_cromer(
    df:         RHSFunc, 
    args:       NDArray[np.float64], 
    n_steps:    float, 
    h:          float, 
    y0:         NDArray[np.float64]
) -> NDArray[np.float64]:
    
    y       = np.zeros( (n_steps, len(y0)), dtype=np.float64 )
    y_cur   = np.zeros( len(y0), dtype=np.float64 )
    dy      = np.zeros( len(y0), dtype=np.float64 )
    
    y[0] = y0

    for i in range(1, n_steps):
        y_prev = y[i-1]
        y_cur  = y[i-1].copy()

        for j in range(len(y0)):
            df(y_cur, args, dy)
            y_cur[j] = y_prev[j] + h * dy[j]

        y[i] = y_cur

    return y

# ================================================================================
@njit
def cd_lorenz(
    args:       NDArray[np.float64], 
    n_steps:    float, 
    h:          float, 
    y0:         NDArray[np.float64]
) -> NDArray[np.float64]:
    
    y = np.zeros( (n_steps, len(args)), dtype=np.float64 )
    y[0] = y0

    sigma, rho, beta = args

    s = 0.5
    h1 = h * s
    h2 = h * (1 - s)

    denom_z = 1.0 + h2 * beta
    denom_y = 1.0 + h2
    denom_x = 1.0 + h2 * sigma

    sigma_h1 = sigma * h1
    sigma_h2 = sigma * h2

    for i in range(n_steps - 1):
        x_i, y_i, z_i = y[i]

        # Explicit half-step
        x_s = x_i + sigma_h1 * (y_i - x_i)
        y_s = y_i + h1 * (x_s * (rho - z_i) - y_i)
        z_s = z_i + h1 * (x_s * y_s - beta * z_i)

        # Implicit half-step (reverse order)
        z_next = (z_s + h2 * x_s * y_s) / denom_z
        y_next = (y_s + h2 * x_s * (rho - z_next)) / denom_y
        x_next = (x_s + sigma_h2 * y_next) / denom_x

        y[i + 1] = [x_next, y_next, z_next]

    return y

# ================================================================================
@njit
def cd_chen(
    args:       NDArray[np.float64], 
    n_steps:    float, 
    h:          float, 
    y0:         NDArray[np.float64]
) -> NDArray[np.float64]:
    
    y = np.zeros( (n_steps, len(args)), dtype=np.float64 )
    y[0] = y0

    a, b, c = args

    s = 0.5
    h1 = h * s
    h2 = h * (1 - s)

    for i in range(n_steps - 1):
        x0, y0, z0 = y[i]

        # --- D1 ---
        x1 = (x0 + h1 * a * y0) / (1 + h1 * a)
        y1 = (y0 + h1 * ((c - a) * x1 - x1 * z0)) / (1 - h1 * c)
        z1 = (z0 + h1 * x1 * y1) / (1 + h1 * b)

        # --- D2 ---
        z2 = z1 + h2 * (x1 * y1 - b * z1)
        y2 = y1 + h2 * ((c - a) * x1 - x1 * z2 + c * y1)
        x2 = x1 + h2 * a * (y2 - x1)

        y[i + 1] = [x2, y2, z2]

    return y

# ================================================================================