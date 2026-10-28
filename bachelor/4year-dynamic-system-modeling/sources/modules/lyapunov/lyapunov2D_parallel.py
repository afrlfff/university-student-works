import numpy as np
from numpy.typing import NDArray
from multiprocessing import Pool
import functools
from tqdm import tqdm # for debug

from modules.systems.typing import RHSFunc 
from modules.integrate import solve_ode, solve_ode_step
from modules.integrate.typing import ODESolver, SOLVER_RK4

def _calculate_max_LLE(
    f: RHSFunc,                         # right-hand side of ODE system
    params_base: NDArray[np.float64],   # base parameters of the system
    y0: NDArray[np.float64],            # initial state vector

    n_record: int,                      # number of steps for LLE computation (after transient)
    n_transient: int,                   # number of transient steps to discard
    h: float,                           # integration step size

    param_idxs: tuple[int, int],        # indexes of target parameters
    pert_var_idx: int,                  # index of dependent state variable to perturb

    r: float,                           # initial perturbation magnitude
    L: int,                             # steps between renormalizations
    norm_var_idxs: list[int],           # variables used in norm computation (None → all)

    solver: ODESolver,                  # ODE solver method
    params_pair: NDArray[np.float64],   # 
) -> np.float64:

    params_current = params_base.copy()
    params_current[param_idxs[0]] = params_pair[0]
    params_current[param_idxs[1]] = params_pair[1]

    y_true      = np.zeros_like(y0)
    y_pert      = np.zeros_like(y0)
    y_pert_prev = np.zeros_like(y0)

    # integrate full
    y = solve_ode(f, params_current, n_transient + n_record, h, y0, solver=solver)
    y = y[n_transient :]
    
    # initial perturbed state
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
                # y_pert = y_true + (y_pert - y_true) * (r / norm)
                for i in range(len(y0)):
                    y_pert[i] = y_true[i] + (y_pert[i] - y_true[i]) * (r / norm)

        
        # update previous perturbed state
        y_pert_prev[:] = y_pert[:]

    return (lle_sum / (steps_used * L * h)) if (steps_used > 0) else (np.nan)
    #return (lle_sum / steps_used) if (steps_used > 0) else (np.nan)


def lyapunov2D_parallel(
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
    n_jobs: int = None                      # num jobs for parallel
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """
    Computes maximal Lyapunov exponent (LLE) over a 2D parameter scan.
    Returns (param1_grid, param2_grid, LLE_grid)
    """

    if norm_var_idxs is None:
        norm_var_idxs = list(range(len(y0)))

    param1_values = np.linspace(param1_range[0], param1_range[1], N).astype(np.float64)
    param2_values = np.linspace(param2_range[0], param2_range[1], N).astype(np.float64)
    param_pairs   = np.array(np.meshgrid(param1_values, param2_values)).T.reshape(-1, 2).astype(np.float64)

    worker = functools.partial(
        _calculate_max_LLE,
        f, params, y0, n_record, n_transient, h, param_idxs, pert_var_idx, r, L, norm_var_idxs, solver
    )

    with Pool(processes=n_jobs) as pool:
        results = list(tqdm(pool.imap(worker, param_pairs), total=len(param_pairs), desc="Processing ..."))

    LLE_grid = np.array(results, dtype=np.float64).reshape(N, N).T

    return (param1_values, param2_values, LLE_grid)