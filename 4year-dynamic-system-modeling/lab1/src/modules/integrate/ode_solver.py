import numpy as np
from typing import Callable

from .methods import *

# ====================================================================================================

class ODESolver:
    def __init__(
        self, 
        f: Callable, args: list,
        tmin: float, tmax: float, dt: float, 
        init_conditions: list 
    ):
        self.f = f
        self.args = args
        self.tmin = tmin
        self.tmax = tmax
        self.dt = dt
        self.init_conditions = np.array(init_conditions, dtype=np.float32)
        self.t = np.arange(tmin, tmax + dt, dt).astype(np.float32)

    def solve(self, method: str) -> np.ndarray:
        solver = self.__str2method(method)
        
        return solver(
            lambda state: self.f(state, self.args), 
            self.t, self.init_conditions
            )

    def __str2method(self, method: str) -> Callable:
        assert method in self.__method_list()

        if method == 'euler': return euler
        if method == 'euler-cromer': return euler_cromer
        if method == 'rk-4': return runge_kutta_4
        if method == 'midpoint': return midpoint
        if method == 'cd-lorenz':
            return lambda df, t, init_conditions: cd_lorenz(t=t, init_conditions=init_conditions, args=self.args)

    def __method_list(self) -> list:
        return ['euler', 'euler-cromer', 'rk-4', 'midpoint', 'cd-lorenz']

# ====================================================================================================
