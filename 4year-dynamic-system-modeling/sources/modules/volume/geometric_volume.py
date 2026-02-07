import numpy as np
from numpy.typing import NDArray
from tqdm import tqdm

from modules.systems.typing import RHSFunc
from modules.integrate import solve_ode_step
from modules.integrate.typing import ODESolver, SOLVER_RK4

def geometric_volume(
    f: RHSFunc,
    params: NDArray[np.float64],

    n_integrate: int,
    h: float,
    
    cloud: NDArray[np.float64],
    solver: ODESolver = SOLVER_RK4,     # method to solve ODE
):
    if cloud.shape[0] < 1:
        raise ValueError("Cloud must contain at least one initial state")
    
    state = np.zeros(cloud.shape[1], dtype=np.float64)
    cloud_copy = cloud.copy()

    Vg = np.zeros(n_integrate)

    for i in tqdm(range(n_integrate), desc="Processing ..."):
        for j in range(cloud_copy.shape[0]):
            solve_ode_step(f, params, h, cloud_copy[j, :], state, solver=solver)
            cloud_copy[j] = state
        cov = np.cov(cloud_copy.T)
        Vg[i] = np.sqrt(np.abs(np.linalg.det(cov)))

    return Vg
