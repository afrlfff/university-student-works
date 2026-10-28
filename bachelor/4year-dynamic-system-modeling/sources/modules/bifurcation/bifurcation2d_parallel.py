import numpy as np
from numpy.typing import NDArray
from scipy.signal import find_peaks
from sklearn.cluster import DBSCAN
from multiprocessing import Pool
import functools
from tqdm import tqdm # for debug

from modules.systems.typing import RHSFunc
from modules.integrate import solve_ode

# ================================================================================

def _solve_single(f, params_base, y0, h, param_idxs, var_idx, n_total, n_transient, solver, dbscan, decimation, threshold, params_pair):
    params_current = params_base.copy()
    params_current[param_idxs[0]] = params_pair[0]
    params_current[param_idxs[1]] = params_pair[1]
    
    # solve ode
    y = solve_ode(f, params_current, n_total, h, y0, solver=solver)
    
    # remove transient + apply decimation + get target variable
    y = y[n_transient::decimation, var_idx]

    # apply threshold limit
    if threshold is not None:
        y = np.clip(y, -threshold, threshold)

    # find peaks
    peak_idxs, _ = find_peaks(y)
    peaks = y[peak_idxs]

    if len(peaks) == 0:
        return 0
    else:
        # dbscan
        labels = dbscan.fit_predict(peaks.reshape(-1, 1))
        cluster_numbers = np.unique(labels).shape[0]

        return cluster_numbers

# ================================================================================

def bifurcation2D_parallel(
    f: RHSFunc,                         # input function (right-hand side of the differential equation)
    params: NDArray[np.float64],        # input function arguments 
    y0: NDArray[np.float64],            # initial conditions (state vector)
    
    n_record: float,                    # number of steps of main recording time (after transient)
    n_transient: float,                 # number of steps of transient time (how much steps will be thrown away)
    h: float,                           # step size
    
    param_idxs: tuple[int, int],        # indexes of target parameters
    param1_range: tuple[float, float],  # range of 1st target parameter changing: (p_min, p_max)
    param2_range: tuple[float, float],  # range of 2nd target parameter changing: (p_min, p_max)
    N : int,                            # resulution of 2D-bifurcation (NxN)
    
    var_idx: int,                       # index of dependent state variable (e.g., var_idx=0 equal to X)

    dbscan_eps: float,                  # epsilon for DBSCAN
    dbscan_min_samples: int,            # min samples for DBSCAN
    
    solver: str = 'cd',                 # method to solve ODE
    decimation: int = 1,                # decimation of calculated points (to get fewer points)
    threshold: float | None = None,     # maximum allowed value of state variable.
    n_jobs=None                         # maximum nubmer of cores for parallel process
) -> np.ndarray:
    # ============================================================================
    n_total = n_record + n_transient

    param1_values = np.linspace(param1_range[0], param1_range[1], N)
    param2_values = np.linspace(param2_range[0], param2_range[1], N)
    param_pairs = np.array(np.meshgrid(param1_values, param2_values)).T.reshape(-1, 2)

    dbscan = DBSCAN(eps=dbscan_eps, min_samples=dbscan_min_samples)
    results = np.zeros(N * N)

    worker = functools.partial(
        _solve_single,
        f, params, y0, h, param_idxs, var_idx, n_total,
        n_transient, solver, dbscan, decimation, threshold
    )

    with Pool(processes=n_jobs) as pool:
        results = list(tqdm(pool.imap(worker, param_pairs), total=len(param_pairs)))

    return np.array(results)