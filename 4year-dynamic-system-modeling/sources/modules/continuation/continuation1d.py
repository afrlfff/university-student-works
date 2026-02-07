import numpy as np
from numpy.typing import NDArray
from tqdm import tqdm # for debug

from modules.systems.typing import RHSFunc
from modules.integrate import solve_ode
from modules.integrate.typing import ODESolver, SOLVER_RK4

def continuation1d(
    f: RHSFunc,
    params: NDArray[np.float64],
    y0: NDArray[np.float64],

    n_record: float,
    n_transient: float,
    h: float,

    param_idx: str,
    param_range: tuple[float, float],
    N: int,
    
    var_idx: int,

    solver: ODESolver = SOLVER_RK4,     # method to solve ODE
):
    result          = np.empty(N, dtype=object)

    param_values    = np.linspace(param_range[0], param_range[1], N)
    state           = y0.copy()
    params_current  = params.copy()

    for i, param_value in enumerate(tqdm(param_values, desc="Processing")):
        params_current[param_idx] = param_value
        
        # integrate transient + sample
        y = solve_ode(f, params_current, n_transient + n_record, h, state, solver=solver)

        # remove transient + extract target variable
        y = y[n_transient :, var_idx]
        
        # find all local maxima
        y_maxima = y[1:-1][(y[1:-1] > y[:-2]) & (y[1:-1] > y[2:])]

        # save result
        result[i] = (y_maxima) if (y_maxima.size > 0) else (np.nan)

        # FORWARD CONTINUATION
        state = y[-1].copy()

    return param_values, result