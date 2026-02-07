import numpy as np
from numpy.typing import NDArray
from tqdm import tqdm # for debug

from modules.systems.typing import RHSFunc 
from modules.integrate import solve_ode, solve_ode_step
from modules.integrate.typing import ODESolver, SOLVER_RK4


def lyapunov1D(
    f: RHSFunc,                             # right-hand side of ODE system
    params: NDArray[np.float64],            # base parameters of the system
    y0: NDArray[np.float64],                # initial state vector

    n_record: int,                          # number of steps for LLE computation (after transient)
    n_transient: int,                       # number of transient steps to discard
    h: float,                               # integration step size

    param_idx: int,                         # index of parameter to scan
    param_range: tuple[float, float],       # (p_min, p_max) for parameter scan
    N: int,                                 # number of parameter values to evaluate

    pert_var_idx: int,                      # index of dependent state variable to perturb

    r: float = 1e-6,                        # initial perturbation magnitude
    L: int = 20,                            # steps between renormalizations
    norm_var_idxs: list[int] | None = None, # variables used in norm computation (None → all)

    solver: ODESolver = SOLVER_RK4,         # ODE solver method
) -> tuple[NDArray[np.float64], np.ndarray]:
    """
    Computes maximal Lyapunov exponent (LLE) over a 1D parameter scan.
    Returns (param_values, LLE_values).
    """

    if norm_var_idxs is None:
        norm_var_idxs = list(range(len(y0)))

    param_values = np.linspace(param_range[0], param_range[1], N)
    LLE_values   = np.zeros(N, dtype=np.float64)

    y_true      = np.zeros_like(y0)
    y_pert      = np.zeros_like(y0)
    y_pert_prev = np.zeros_like(y0)

    params_current = params.copy()

    for i, p in enumerate(tqdm(param_values, desc="Processing ...")):
        params_current[param_idx] = p

        # integrate full
        y = solve_ode(f, params_current, n_transient + n_record, h, y0, solver=solver)
        y = y[n_transient :]
        
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

        LLE_values[i] = (lle_sum / (steps_used * L * h)) if (steps_used > 0) else (np.nan)

    return (param_values, LLE_values)