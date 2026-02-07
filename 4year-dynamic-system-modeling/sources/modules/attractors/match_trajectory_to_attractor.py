import numpy as np
from numpy.typing import NDArray
from scipy.spatial.distance import cdist

def match_trajectory_to_attractor(
    trajectory: NDArray[np.float64],
    attr_trajectory: NDArray[np.float64]
) -> np.float64:
    # all paired distances between points of attractor trajectories and trajectory points
    dists = cdist(trajectory, attr_trajectory)  # (n_traj_points, n_attr_points)
    
    # find closest attractor point for each trajectory point and save its distance 
    min_dists = np.min(dists, axis=1) # (n_traj_points, )

    # save mean of found distances as a coefficient of similarity of two attractors 
    return np.mean(min_dists)  # (1, )