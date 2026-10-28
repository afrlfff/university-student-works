import numpy as np
from numpy.typing import NDArray
from tqdm import tqdm
from multiprocessing import Pool
import functools
from modules.systems.typing import RHSFunc
from modules.integrate import solve_ode
from modules.integrate.typing import ODESolver, SOLVER_RK4
from modules.attractors import match_trajectory_to_attractor

# ================================================================================

def attraction_basins(
    f: RHSFunc,                                 # input function (right-hand side of the differential equation)
    params: NDArray[np.float64],                # input function arguments 
    init_conditions: NDArray[np.float64],       # initial conditions (state vector)
    attr_init_conditions: NDArray[np.float64],  # Initial conditions known to converge to reference attractors
    
    n_record: int,                              # number of steps of main recording time (after transient)
    n_transient: int,                           # number of steps of transient time (how much steps will be thrown away)
    h: float,                                   # step size

    n_match_points: int = 1,                    # number of final trajectory points used to match against attractors
    solver: ODESolver = SOLVER_RK4,             # method to solve ODE
    debug: bool = False                         # show / don't show debug messages 
):
    # constants
    n_attractors        = len(attr_init_conditions)
    n_init_conditions   = len(init_conditions)

    # initialize results
    result_matches          = np.zeros(n_init_conditions,               dtype=int)
    attractor_trajectories  = np.zeros((n_attractors, n_record, 3),     dtype=np.float64)
    mean_dists              = np.zeros(n_attractors,                    dtype=np.float64)

    # evenly distribute indexes to check match against attractor
    match_idxs = np.round(np.linspace(0, n_record - 1, n_match_points)).astype(int)

    # integrate attractors trajectory
    iterator = (tqdm(attr_init_conditions, desc="Integrate attractors ...")) if (debug) else (attr_init_conditions)
    for i, attr_init_condition in enumerate(iterator):
        y = solve_ode(f, params, n_record + n_transient, h, attr_init_condition, solver=solver)
        attractor_trajectories[i] = y[n_transient: ]

    # calculate matches
    iterator = (tqdm(init_conditions, desc="Calculate matches ...")) if (debug) else (init_conditions)
    for i, init_condition in enumerate(iterator):
        # integrate (now "y" is an attactor of current initial condition)
        y = solve_ode(f, params, n_transient + n_record, h, init_condition, solver=solver)
        y = y[n_transient: ]

        # get points to check match
        test_points = y[match_idxs]  # (n_match_points, 3)

        # find mean distances from test_points to each attractor trajectory
        for a in range(n_attractors):
            mean_dists[a] = match_trajectory_to_attractor(test_points, attractor_trajectories[a])
        
        # save index of closest attractor (index of attractor which has a minimum mean distance)
        result_matches[i] = np.argmin(mean_dists)

    return result_matches

# ================================================================================

def _process_one(f, params, n_record, n_transient, h, solver, attractor_trajectories, match_idxs, y0):
    # constants
    n_attractors = attractor_trajectories.shape[0]

    # init result
    mean_dists = np.zeros(n_attractors, dtype=np.float64)

    # integrate (now "y" is an attactor of current initial condition)
    y = solve_ode(f, params, n_transient + n_record, h, y0, solver=solver)
    y = y[n_transient: ]

    # get points to check match
    test_points = y[match_idxs]  # (n_match_points, 3)

    # find mean distances from test_points to each attractor trajectory
    for a in range(n_attractors):
        mean_dists[a] = match_trajectory_to_attractor(test_points, attractor_trajectories[a])
    
    # save index of closest attractor (index of attractor which has a minimum mean distance)
    return np.argmin(mean_dists)

# ================================================================================

def attraction_basins_parallel(
    f: RHSFunc,                                 # input function (right-hand side of the differential equation)
    params: NDArray[np.float64],                # input function arguments 
    init_conditions: NDArray[np.float64],       # initial conditions (state vector)
    attr_init_conditions: NDArray[np.float64],  # Initial conditions known to converge to reference attractors
    
    n_record: int,                              # number of steps of main recording time (after transient)
    n_transient: int,                           # number of steps of transient time (how much steps will be thrown away)
    h: float,                                   # step size

    n_match_points: int = 1,                    # number of final trajectory points used to match against attractors
    solver: ODESolver = SOLVER_RK4,             # method to solve ODE
    n_jobs: int | None = None,
    debug: bool = False                         # show / don't show debug messages 
):
    # constants
    n_attractors = len(attr_init_conditions)

    # initialize results
    attractor_trajectories = np.zeros((n_attractors, n_record, 3), dtype=np.float64)

    # evenly distribute indexes to check match against attractor
    match_idxs = np.round(np.linspace(0, n_record - 1, n_match_points)).astype(int)

    # integrate attractors trajectory
    iterator = (tqdm(attr_init_conditions, desc="Integrate attractors ...")) if (debug) else (attr_init_conditions)
    for i, attr_init_condition in enumerate(iterator):
        y = solve_ode(f, params, n_record + n_transient, h, attr_init_condition, solver=solver)
        attractor_trajectories[i] = y[n_transient: ]

    # calculate matches
    worker = functools.partial(_process_one, f, params, n_record, n_transient, h, solver, attractor_trajectories, match_idxs)
    with Pool(processes=n_jobs) as pool:
        if debug:
            matches = list(tqdm(pool.imap(worker, init_conditions), total=len(init_conditions), desc="Calculate matches ..."))
        else:
            matches = list(pool.imap(worker, init_conditions))

    matches = np.array(matches, dtype=int)
    return matches

# ================================================================================