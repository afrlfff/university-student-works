import numpy as np
import hashlib
from pathlib import Path
from typing import Optional, Callable

from methods import *

# ====================================================================================================

class Integrator:
    def __init__(
        self, 
        f: Callable, 
        tmin: float, tmax: float, dt: float, 
        init_conditions: list    
    ):
        self.f = f
        self.tmin = tmin
        self.tmax = tmax
        self.dt = dt
        self.init_conditions = np.array(init_conditions, dtype=np.float32)
        self.t = np.arange(tmin, tmax + dt, dt).astype(np.float32)

        self.method = None

    def set_method(self, method: str):
        assert method in self.__method_list()

        self.method = self.__str2method(method)

    def run(self) -> np.ndarray:
        assert self.method is not None

        return self.method(self.f, self.t, self.init_conditions)

    def __str2method(self, method: str) -> Callable:
        assert method in self.__method_list()

        if method == 'euler': return euler_explicit
        if method == 'euler-cromer': return euler_cromer
        if method == 'runge-kutta-2': return runge_kutta_2
        if method == 'runge-kutta-4': return runge_kutta_4
        if method == 'midpoint': return midpoint
        if method == 'cd-lorenz':
            return lambda df, t, init_conditions: cd_lorenz(t, init_conditions, params=(10, 28, 8/3))

    def __method_list(self) -> list:
        return ['euler', 'euler-cromer', 'runge-kutta-2', 'runge-kutta-4', 'midpoint', 'cd-lorenz']

# ====================================================================================================

class IntegratorCacher:
    def __init__(self, cache_dir: str | Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    # ================================================================================================
    def _make_key(self, integrator: Integrator) -> str:
        
        parts = [
            integrator.f.__name__,
            integrator.method.__name__,
            f"{integrator.tmin:.6f}",
            f"{integrator.tmax:.6f}",
            f"{integrator.dt:.10f}",
            str(tuple(integrator.init_conditions))
        ]
        key_str = "_".join(parts)
        
        return hashlib.sha256(key_str.encode()).hexdigest()
    # ================================================================================================
    def save(self, integrator: Integrator, result: np.ndarray) -> None:

        key = self._make_key(integrator)
        filepath = self.cache_dir / f"{key}.npy"
        np.save(filepath, result, allow_pickle=False)
    # ================================================================================================
    def get(self, integrator: Integrator) -> Optional[np.ndarray]:
        
        key = self._make_key(integrator)
        filepath = self.cache_dir / f"{key}.npy"
        if filepath.is_file():
            return np.load(filepath, allow_pickle=False)
        return None
    # ================================================================================================
