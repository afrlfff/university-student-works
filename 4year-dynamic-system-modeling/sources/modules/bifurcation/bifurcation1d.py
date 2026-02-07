import numpy as np
from numpy.typing import NDArray
from scipy.signal import find_peaks
from tqdm import tqdm # for debug

from modules.systems.typing import RHSFunc
from modules.integrate import solve_ode
from modules.integrate.typing import ODESolver, SOLVER_RK4

# ================================================================================

def bifurcation1D(
    f: RHSFunc,                         # input function (right-hand side of the differential equation)
    params: NDArray[np.float64],        # input function arguments 
    y0: NDArray[np.float64],            # initial conditions (state vector)
    
    n_record: float,                    # number of steps of main recording time (after transient)
    n_transient: float,                 # number of steps of transient time (how much steps will be thrown away)
    h: float,                           # step size
    
    param_idx: int,                     # index of target parameter
    param_range: tuple[float, float],   # range of target parameter changing: (p_min, p_max)
    N : int,                            # resulution of 1D-bifurcation
    
    var_idx: int,                       # index of dependent state variable (e.g., var_idx=0 equal to X)
    
    solver: ODESolver = SOLVER_RK4,     # method to solve ODE
    decimation: int = 1,                # decimation of calculated points (to get fewer points)
    threshold: float | None = None,     # maximum allowed value of state variable.
) -> np.ndarray:
    # ============================================================================
    n_total = n_record + n_transient

    param_values = np.linspace(param_range[0], param_range[1], N)
    params_current = params.copy()

    results = np.empty(N, dtype=object) # array of pointers to arrays of peaks
    
    #for i, param_value in enumerate(param_values):
    for i, param_value in enumerate(tqdm(param_values, desc="Processing")): # temp
        params_current[param_idx] = param_value

        # solve ode
        y = solve_ode(f, params_current, n_total, h, y0, solver=solver)
        
        # remove transient + apply decimation + get target variable
        y = y[n_transient::decimation, var_idx]

        # apply threshold limit
        if threshold is not None:
            y = np.clip(y, -threshold, threshold)

        # find peaks
        peak_idxs, _ = find_peaks(y)

        results[i] = y[peak_idxs]
    
    return results