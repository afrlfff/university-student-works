import numpy as np
from numpy.typing import NDArray
from scipy.signal import find_peaks
from sklearn.cluster import DBSCAN
from tqdm import tqdm # for debug

from modules.systems.typing import RHSFunc
from modules.integrate.typing import ODESolver, SOLVER_RK4
from modules.integrate import solve_ode

# ================================================================================

def bifurcation2D(
    f: RHSFunc,                        # input function (right-hand side of the differential equation)
    params: NDArray[np.float64],       # input function arguments 
    y0: NDArray[np.float64],           # initial conditions (state vector)
    
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
    
    solver: ODESolver = SOLVER_RK4,     # method to solve ODE
    decimation: int = 1,                # decimation of calculated points (to get fewer points)
    threshold: float | None = None,     # maximum allowed value of state variable.
) -> np.ndarray:
    # ============================================================================
    n_total = n_record + n_transient

    param1_values = np.linspace(param1_range[0], param1_range[1], N).astype(np.float64)
    param2_values = np.linspace(param2_range[0], param2_range[1], N).astype(np.float64)
    param_pairs = np.array(np.meshgrid(param1_values, param2_values)).T.reshape(-1, 2).astype(np.float64)
    params_current = params.copy()
    
    dbscan = DBSCAN(eps=dbscan_eps, min_samples=dbscan_min_samples)

    results = np.zeros(N * N, dtype=np.float64)

    #for i, (param1_value, param2_value) in enumerate(param_pairs):
    for i, (param1_value, param2_value) in enumerate(tqdm(param_pairs, desc="Solve ODE ...")): # temp
        params_current[param_idxs[0]] = param1_value
        params_current[param_idxs[1]] = param2_value

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
            results[i] = 0
        else:
            # dbscan
            labels = dbscan.fit_predict(peaks.reshape(-1, 1))
            cluster_numbers = np.unique(labels).shape[0]

            results[i] = cluster_numbers

    return results