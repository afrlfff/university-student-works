import numpy as np
from numpy.typing import NDArray
from multiprocessing import Pool
import functools
from scipy.spatial.distance import pdist
from tqdm import tqdm
from modules.integrate import solve_ode
from modules.systems.typing import RHSFunc
from modules.integrate.typing import ODESolver, SOLVER_RK4

# ==============================================================================

def _max_pairwise_distance(points: np.ndarray) -> float:
    if points.shape[0] < 2:
        return 0.0
    return np.max(pdist(points))

# ==============================================================================

def find_attractors_by_diameter(
    f: RHSFunc,                             # input function (right-hand side of the differential equation)
    params: NDArray[np.float64],            # input function arguments 
    init_conditions: NDArray[np.float64],   # array of initial conditions (state vectors)
    
    n_record: int,                          # number of steps of main recording time (after transient)
    n_transient: int,                       # number of steps of transient time (how much steps will be thrown away)
    h: float,                               # step size

    eps: float = 1.0,                       # minimum difference between different attractors
    
    solver: ODESolver = SOLVER_RK4,         # method to solve ODE
    debug: bool = False,                    # show / don't show debug messages
):
    # constants
    n_init_conditions = init_conditions.shape[0]

    # init results
    diameters       = np.zeros(n_init_conditions, dtype=np.float64)
    used_diameters  = np.zeros(n_init_conditions, dtype=np.bool)
    results         = []

    # integrate + calculate diameters
    iterator = (tqdm(init_conditions, desc="Integrate + calculate diameters ...")) if (debug) else (init_conditions)
    for i, y0 in enumerate(iterator):
        y = solve_ode(f, params, n_transient + n_record, h, y0, solver)
        y = y[n_transient: ]
        diameters[i] = _max_pairwise_distance(y)
    
    # find unique attractors
    iterator = (tqdm(range(n_init_conditions), desc="Find unique attractors ...")) if (debug) else (range(n_init_conditions))
    for i in iterator:
        if used_diameters[i]:
            continue
        
        cluster_mask = np.abs(diameters - diameters[i]) < eps
        used_diameters[cluster_mask] = True
        
        results.append(init_conditions[i])

    return np.array(results, dtype=np.float64)

# ==============================================================================

def _process_one(f, params, n_transient, n_record, h, solver, init_condition):
    y = solve_ode(f, params, n_transient + n_record, h, init_condition, solver)
    return _max_pairwise_distance(y[n_transient: ])

# ==============================================================================

def find_attractors_by_diameter_parallel(
    f: RHSFunc,                             # input function (right-hand side of the differential equation)
    params: NDArray[np.float64],            # input function arguments 
    init_conditions: NDArray[np.float64],   # array of initial conditions (state vectors)
    
    n_record: int,                          # number of steps of main recording time (after transient)
    n_transient: int,                       # number of steps of transient time (how much steps will be thrown away)
    h: float,                               # step size

    eps: float = 1.0,                       # minimum difference between different attractors
    
    solver: ODESolver = SOLVER_RK4,         # method to solve ODE
    n_jobs: int | None = None,              # number of used CPU cores (`None` equal to maximum available)
    debug: bool = False,                    # show / don't show debug messages
):
    # constants
    n_init_conditions = init_conditions.shape[0]

    # parallel integrating
    worker = functools.partial(_process_one, f, params, n_transient, n_record, h, solver)
    with Pool(processes=n_jobs) as pool:
        if debug:
            diameters = list(tqdm(pool.imap(worker, init_conditions), total=len(init_conditions), desc="Integrate + calculate diameters ..."))
        else:
            diameters = list(pool.imap(worker, init_conditions))

    # init results
    diameters       = np.array(diameters, dtype=np.float64)
    used_diameters  = np.zeros(n_init_conditions, dtype=np.bool)
    results         = []
    
    # find unique attractors
    iterator = (tqdm(range(n_init_conditions), desc="Find unique attractors ...")) if (debug) else (range(n_init_conditions))
    for i in iterator:
        if used_diameters[i]:
            continue
        
        cluster_mask = np.abs(diameters - diameters[i]) < eps
        used_diameters[cluster_mask] = True
        
        results.append(init_conditions[i])

    return np.array(results, dtype=np.float64)
