import numpy as np
from numpy.typing import NDArray
from tqdm import tqdm

from modules.integrate import solve_ode_step
from modules.systems.typing import RHSFunc
from modules.integrate.typing import ODESolver, SOLVER_RK4

# ==============================================================================

def sync_slave_time_symmetric(
    f: RHSFunc,
    params: NDArray[np.float64],
    y0: NDArray[np.float64],

    h: float,

    y_master: NDArray[np.float64],

    n_iter: int,
    n_window: float,
    K_forw: float,
    K_back: float,

    sync_var_idx: int = 0,

    solver: ODESolver = SOLVER_RK4,
    debug: bool = False,
) -> np.typing.NDArray[np.float64]:

    # init results
    y_fwd = np.zeros((n_window, 3), dtype=np.float64)
    y_bwd = np.zeros((n_window, 3), dtype=np.float64)

    # set init conditions
    y_fwd[0] = y0

    # synchronization loop
    iterator = (tqdm(range(n_iter), desc="Syncronization ...")) if (debug) else (range(n_iter))
    for i in iterator:
        # Forward sync: slave follows master in forward time
        for j in range(1, n_window):
            solve_ode_step(f, params, h, y_fwd[j - 1], y_fwd[j], solver=solver)

            # sync using Pecora-Carrol method
            controller = K_forw * (y_master[j - 1, sync_var_idx] - y_fwd[j - 1, sync_var_idx])
            y_fwd[j, sync_var_idx] += controller * h

        # Backward sync: slave follows master in backward time
        y_bwd[0] = y_fwd[-1]
        for j in range(1, n_window):
            solve_ode_step(f, params, -h, y_bwd[j - 1], y_bwd[j], solver=solver)

            # sync using Pecora-Carrol method
            controller = -K_back * (y_master[n_window - j, sync_var_idx] - y_bwd[j - 1, sync_var_idx])
            y_bwd[j, sync_var_idx] -= controller * h
        
        # update y_fwd first state
        y_fwd[0] = y_bwd[-1]
    
    # return last forward trajectory as a result of slave system
    return y_fwd

# ==============================================================================

# def sync_slave_time_symmetric(
#     f: RHSFunc,
#     params: NDArray[np.float64],
#     y0: NDArray[np.float64],

#     h: float,

#     y_master: NDArray[np.float64],

#     n_iter: int,
#     n_window: float,
#     K_forw: float,
#     K_back: float,

#     solver: ODESolver = SOLVER_RK4,
#     debug: bool = False,
# ) -> np.typing.NDArray[np.float64]:

#     # init results
#     y_fwd = np.zeros((n_window, 3), dtype=np.float64)
#     y_bwd = np.zeros((n_window, 3), dtype=np.float64)

#     # synchronization loop
#     iterator = (tqdm(range(n_iter), desc="Syncronization ...")) if (debug) else (range(n_iter))
#     for i in iterator:
#         # Forward sync: slave follows master in forward time
#         y_fwd[0] = (y0) if (i == 0) else (y_bwd[-1])
#         for j in range(1, n_window):
#             slave_prev  = y_fwd[j - 1]
#             master_prev = y_master[j - 1]

#             solve_ode_step(f, params, h, slave_prev, y_fwd[j], solver=solver)

#             # sync using Pecora-Carrol method
#             controller = K_forw * (master_prev - slave_prev)
#             y_fwd[j] += controller * h

#         # Backward sync: slave follows master in backward time
#         y_bwd[0] = y_fwd[-1]
#         for j in range(1, n_window):
#             slave_prev  = y_bwd[j - 1]
#             master_prev = y_master[n_window - 1 - (j - 1)] # y_master[n_window - 1 - j]

#             solve_ode_step(f, params, -h, slave_prev, y_bwd[j], solver=solver)

#             # sync using Pecora-Carrol method
#             controller = -K_back * (master_prev - slave_prev)
#             y_bwd[j] += controller * -h
    
#     y_fwd[0] = y0
#     return y_fwd.copy()