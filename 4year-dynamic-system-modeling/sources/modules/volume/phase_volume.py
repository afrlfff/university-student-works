import numpy as np
from numpy.typing import NDArray
from tqdm import tqdm

from modules.systems.typing import RHSFunc
from modules.integrate import solve_ode_step
from modules.integrate.typing import ODESolver, SOLVER_RK4

def phase_volume(
    f: RHSFunc,
    params: NDArray[np.float64],

    n_integrate: int,
    h: float,
    
    cloud: NDArray[np.float64],
    solver: ODESolver = SOLVER_RK4,     # method to solve ODE
):
    if cloud.shape[0] < 3:
        raise ValueError("Cloud must contain at least three initial states")

    # центральная траектория
    center = cloud.mean(axis=0)

    # три инфинитезимальных вектора
    v0 = cloud[0] - center
    v1 = cloud[1] - center
    v2 = cloud[2] - center

    # нормировка
    eps_norm = np.linalg.norm(v0)
    v0 /= eps_norm
    v1 /= eps_norm
    v2 /= eps_norm

    Vp = np.zeros(n_integrate)

    y0 = np.zeros(cloud.shape[1], dtype=np.float64)
    y1 = np.zeros(cloud.shape[1], dtype=np.float64)
    y2 = np.zeros(cloud.shape[1], dtype=np.float64)
    y3 = np.zeros(cloud.shape[1], dtype=np.float64)

    for i in tqdm(range(n_integrate), desc="Processing ..."):
        # шаг центральной траектории
        solve_ode_step(f, params, h, center, y0, solver=solver)

        # шаги возмущённых траекторий
        solve_ode_step(f, params, h, (y0[0] + v0[0], y0[1] + v0[1], y0[2] + v0[2]), y1, solver=solver)
        solve_ode_step(f, params, h, (y0[0] + v1[0], y0[1] + v1[1], y0[2] + v1[2]), y2, solver=solver)
        solve_ode_step(f, params, h, (y0[0] + v2[0], y0[1] + v2[1], y0[2] + v2[2]), y3, solver=solver)

        w0 = np.array([y1[0] - y0[0], y1[1] - y0[1], y1[2] - y0[2]])
        w1 = np.array([y2[0] - y0[0], y2[1] - y0[1], y2[2] - y0[2]])
        w2 = np.array([y3[0] - y0[0], y3[1] - y0[1], y3[2] - y0[2]])

        V = abs(np.dot(w0, np.cross(w1, w2)))
        Vp[i] = V

        norm0 = np.linalg.norm(w0)
        norm1 = np.linalg.norm(w1)
        norm2 = np.linalg.norm(w2)
        if norm0 > 0:
            v0 = w0 / norm0
        if norm1 > 0:
            v1 = w1 / norm1
        if norm2 > 0:
            v2 = w2 / norm2

    return Vp
