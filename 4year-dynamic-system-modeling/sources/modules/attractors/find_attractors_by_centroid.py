import numpy as np
from numpy.typing import NDArray
from multiprocessing import Pool
import functools
from tqdm import tqdm
from modules.integrate import solve_ode
from modules.systems.typing import RHSFunc
from modules.integrate.typing import ODESolver, SOLVER_RK4

# ==============================================================================

def find_attractors_by_centroid(
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
    centroids       = np.zeros((n_init_conditions, 3), dtype=np.float64)
    used_centroids  = np.zeros(n_init_conditions, dtype=np.bool)
    results         = []

    # integrate init conditions and save centroids
    iterator = (tqdm(init_conditions, desc="Integrating + calculate centroids ...")) if (debug) else (init_conditions)
    for i, y0 in enumerate(iterator):
        y = solve_ode(f, params, n_transient + n_record, h, y0, solver)
        centroids[i] = np.mean(y[n_transient: ], axis=0)

    # find all unique centroids
    iterator = (tqdm(range(n_init_conditions), desc="Find unique attractors ...")) if (debug) else (range(n_init_conditions))
    for i in iterator:
        if used_centroids[i]:
            continue

        distances = np.linalg.norm(centroids - centroids[i], axis=1)
        cluster_mask = distances < eps
        used_centroids[cluster_mask] = True
        
        results.append(init_conditions[i])

    return np.array(results, dtype=np.float64)

# ==============================================================================

def _process_one(f, params, n_transient, n_record, h, solver, y0):
    y = solve_ode(f, params, n_transient + n_record, h, y0, solver)
    return np.mean(y[n_transient: ], axis=0)

# ==============================================================================

def find_attractors_by_centroid_parallel(
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
            centroids = list(tqdm(pool.imap(worker, init_conditions), total=n_init_conditions, desc="Integrating + calculate centroids ..."))
        else:
            centroids = list(pool.imap(worker, init_conditions))
    
    # init results
    centroids       = np.array(centroids, dtype=np.float64)
    used_centroids  = np.zeros(n_init_conditions, dtype=np.bool)
    results         = []

    # find unique all centroids
    iterator = (tqdm(range(n_init_conditions), desc="Find unique attractors ...")) if (debug) else (range(n_init_conditions))
    for i in iterator:
        if used_centroids[i]:
            continue

        distances = np.linalg.norm(centroids - centroids[i], axis=1)
        cluster_mask = distances < eps
        used_centroids[cluster_mask] = True
        
        results.append(init_conditions[i])

    return np.array(results, dtype=np.float64)

# ==============================================================================

