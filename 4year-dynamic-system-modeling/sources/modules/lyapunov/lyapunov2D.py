import numpy as np
from numpy.typing import NDArray
from tqdm import tqdm # for debug

from modules.systems.typing import RHSFunc 
from modules.integrate import solve_ode, solve_ode_step
from modules.integrate.typing import ODESolver, SOLVER_RK4


def lyapunov2D(
    f: RHSFunc,                             # right-hand side of ODE system
    params: NDArray[np.float64],            # base parameters of the system
    y0: NDArray[np.float64],                # initial state vector

    n_record: int,                          # number of steps for LLE computation (after transient)
    n_transient: int,                       # number of transient steps to discard
    h: float,                               # integration step size

    param_idxs: tuple[int, int],            # indexes of target parameters
    param1_range: tuple[float, float],      # range of 1st target parameter changing: (p_min, p_max)
    param2_range: tuple[float, float],      # range of 2nd target parameter changing: (p_min, p_max)
    N : int,                                # resulution of 2D-bifurcation (NxN)

    pert_var_idx: int,                      # index of dependent state variable to perturb

    r: float = 1e-6,                        # initial perturbation magnitude
    L: int = 20,                            # steps between renormalizations
    norm_var_idxs: list[int] | None = None, # variables used in norm computation (None → all)

    solver: ODESolver = SOLVER_RK4,         # ODE solver method
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """
    Computes maximal Lyapunov exponent (LLE) over a 2D parameter scan.
    Returns (param1_grid, param2_grid, LLE_grid)
    """

    if norm_var_idxs is None:
        norm_var_idxs = list(range(len(y0)))

    param1_values = np.linspace(param1_range[0], param1_range[1], N)
    param2_values = np.linspace(param2_range[0], param2_range[1], N)
    param_pairs   = np.array(np.meshgrid(param1_values, param2_values)).T.reshape(-1, 2)
    params_current = params.copy()

    y_true      = np.zeros_like(y0)
    y_pert      = np.zeros_like(y0)
    y_pert_prev = np.zeros_like(y0)

    LLE_grid = np.zeros((N, N), dtype=np.float64)

    for i, (param1_value, param2_value) in enumerate(tqdm(param_pairs, desc="Processing ...")): # temp
        params_current[param_idxs[0]] = param1_value
        params_current[param_idxs[1]] = param2_value

        # integrate full trajectory (transient + recording)
        y = solve_ode(f, params_current, n_transient + n_record, h, y0, solver=solver)
        y = y[n_transient: ]

        # initial state
        y_pert_prev[:] = y[0, :]
        y_pert_prev[pert_var_idx] += r

        lle_sum = 0.0
        steps_used = 0

        for s in range(1, n_record):
            # advance perturbed trajectory
            y_true = y[s]             
            solve_ode_step(f, params_current, h, y_pert_prev, y_pert, solver=solver)

            if s % L == 0:
                # compute norm over selected variables
                diff = y_true[norm_var_idxs] - y_pert[norm_var_idxs]
                norm = np.linalg.norm(diff)

                growth = norm / r
                if growth > 0:
                    lle_sum += np.log(growth)
                    steps_used += 1

                    # renormalize perturbation
                    y_pert = y_true + (y_pert - y_true) * (r / norm)
        
            # update previous perturbed state
            y_pert_prev[:] = y_pert[:]

        #total_time = steps_used * L * h
        LLE_grid[i%N, i//N] = (lle_sum / steps_used) if (steps_used > 0) else (np.nan)

    return (param1_values, param2_values, LLE_grid)