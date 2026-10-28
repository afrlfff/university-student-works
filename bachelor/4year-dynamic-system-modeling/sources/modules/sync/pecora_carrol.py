import numpy as np
from numpy.typing import NDArray
from tqdm import tqdm

from modules.integrate import solve_ode_step
from modules.systems.typing import RHSFunc
from modules.integrate.typing import ODESolver, SOLVER_RK4

# ==============================================================================

def sync_slave_pecora_carrol(
    f: RHSFunc,                         # input function (right-hand side of the differential equation)
    params: NDArray[np.float64],        # input function arguments 
    y0: NDArray[np.float64],            # initial conditions (state vector)
    
    n_steps: int,                       # number of steps of integration time
    h: float,                           # step size
    
    y_master: NDArray[np.float64],      # master trajectory
    sync_coeff: float,                  # synchronize coefficient
    sync_var_idx: int,                  # index of state variable to synchronize

    solver: ODESolver = SOLVER_RK4,     # method to solve ODE
    debug: bool = False,                # show / don't show debug messages
) -> np.typing.NDArray[np.float64]:
    
    y_slave = np.zeros( (n_steps, len(y0)), dtype=np.float64 )
    y_slave[0] = y0
    
    iterator = (tqdm(range(1, n_steps), desc="Syncronization ...")) if (debug) else (range(1, n_steps))
    for i in iterator:
        solve_ode_step(f, params, h, y_slave[i - 1], y_slave[i], solver=solver)

        controller = sync_coeff * (y_master[i - 1, sync_var_idx] - y_slave[i - 1, sync_var_idx])
        y_slave[i, sync_var_idx] += controller * h
    
    return y_slave

# ==============================================================================

def sync_master_slave_pecora_carrol(
    f: RHSFunc,                         # input function (right-hand side of the differential equation)
    params: NDArray[np.float64],        # input function arguments 
    y0_slave: NDArray[np.float64],      # slave initial conditions (state vector)
    y0_master: NDArray[np.float64],     # master initial conditions (state vector)
    
    n_steps: int,                       # number of steps of integration time
    h: float,                           # step size
    
    sync_coeff: float,                  # synchronize coefficient
    sync_var_idx: int,                  # index of state variable to synchronize

    solver: ODESolver = SOLVER_RK4,     # method to solve ODE
    debug: bool = False,                # show / don't show debug messages
) -> np.typing.NDArray[np.float64]:
    
    y_s = np.zeros( (n_steps, len(y0_slave)), dtype=np.float64 )
    y_m = np.zeros( (n_steps, len(y0_master)), dtype=np.float64 )
    
    y_s[0] = y0_slave
    y_m[0] = y0_master
    
    iterator = (tqdm(range(1, n_steps), desc="Syncronization ...")) if (debug) else (range(1, n_steps))
    for i in iterator:
        y_s_prev = y_s[i - 1]
        y_m_prev = y_m[i - 1]
        
        solve_ode_step(f, params, h, y_s[i - 1], y_s[i], solver=solver)
        solve_ode_step(f, params, h, y_m[i - 1], y_m[i], solver=solver)

        controller_s = sync_coeff * (y_m_prev[sync_var_idx] - y_s_prev[sync_var_idx])
        controller_m = sync_coeff * (y_s_prev[sync_var_idx] - y_m_prev[sync_var_idx])
        
        y_s[i, sync_var_idx] += controller_s * h
        y_m[i, sync_var_idx] += controller_m * h
    
    return np.array([y_s, y_m], dtype=np.float64)

# ==============================================================================