import numpy as np
from numpy.typing import NDArray
from modules.systems.typing import RHSFunc
from modules.integrate.typing import ODESolver, SOLVER_RK4
from .typing import COMPARSION_METHOD, METHOD_CENTROID, METHOD_DIAMETER
from .find_attractors_by_centroid import find_attractors_by_centroid, find_attractors_by_centroid_parallel
from .find_attractors_by_diameter import find_attractors_by_diameter, find_attractors_by_diameter_parallel

# ==============================================================================

def find_attractors(
    f: RHSFunc,                             # input function (right-hand side of the differential equation)
    params: NDArray[np.float64],            # input function arguments 
    init_conditions: NDArray[np.float64],   # array of initial conditions (state vectors)
    
    n_record: int,                          # number of steps of main recording time (after transient)
    n_transient: int,                       # number of steps of transient time (how much steps will be thrown away)
    h: float,                               # step size

    eps: float = 1.0,                       # minimum difference between different attractors
    method: COMPARSION_METHOD = METHOD_CENTROID, # method to distinguish attractors
    solver: ODESolver = SOLVER_RK4,         # method to solve ODE    
    debug: bool = False,                    # show / don't show debug messages
):
    if method == METHOD_CENTROID:
        return find_attractors_by_centroid(f, params, init_conditions, n_record, n_transient, h, eps=eps, solver=solver, debug=debug)
    elif method == METHOD_DIAMETER:
        return find_attractors_by_diameter(f, params, init_conditions, n_record, n_transient, h, eps=eps, solver=solver, debug=debug)
    else:
        raise ValueError("Unknown comaprsion method")
    
# ==============================================================================

def find_attractors_parallel(
    f: RHSFunc,                             # input function (right-hand side of the differential equation)
    params: NDArray[np.float64],            # input function arguments 
    init_conditions: NDArray[np.float64],   # array of initial conditions (state vectors)
    
    n_record: float,                        # number of steps of main recording time (after transient)
    n_transient: float,                     # number of steps of transient time (how much steps will be thrown away)
    h: float,                               # step size

    eps: float = 1.0,                       # minimum difference between different attractors
    method: COMPARSION_METHOD = METHOD_CENTROID, # method to distinguish attractors
    solver: ODESolver = SOLVER_RK4,         # method to solve ODE
    n_jobs: int | None = None,              # number of used CPU cores (`None` equal to maximum available)
    debug: bool = False,                    # show / don't show debug messages
):
    if method == METHOD_CENTROID:
        return find_attractors_by_centroid_parallel(f, params, init_conditions, n_record, n_transient, h, eps=eps, solver=solver, debug=debug, n_jobs=n_jobs)
    elif method == METHOD_DIAMETER:
        return find_attractors_by_diameter_parallel(f, params, init_conditions, n_record, n_transient, h, eps=eps, solver=solver, debug=debug, n_jobs=n_jobs)
    else:
        raise ValueError("Unknown comaprsion method")

# ==============================================================================