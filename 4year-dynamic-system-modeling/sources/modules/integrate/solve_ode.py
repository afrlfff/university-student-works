import numpy as np
from numpy.typing import NDArray

from modules.systems.typing import RHSFunc
from .solvers_step import *
from .solvers import *
from .typing import *

# ================================================================================
def solve_ode_step(
    f:          RHSFunc,                # input function (right-hand side of the differential equation)
    args:       NDArray[np.float64],    # input function arguments
    h:          float,                  # step size
    y:          NDArray[np.float64],    # current state buffer
    y_next:     NDArray[np.float64],    # prellocated buffer for the next state
    solver: ODESolver = SOLVER_RK4      # solver
) -> None:
    
    if solver == SOLVER_CD_LORENZ:      return cd_step_lorenz(args, h, y, y_next)
    if solver == SOLVER_CD_CHEN:        return cd_step_chen(args, h, y, y_next)
    
    if solver == SOLVER_EULER:          return euler_step(f, args, h, y, y_next)
    if solver == SOLVER_EULER_CROMER:   return euler_cromer_step(f, args, h, y, y_next)
    if solver == SOLVER_RK4:            return runge_kutta_4_step(f, args, h, y, y_next)
    if solver == SOLVER_MIDPOINT:       return midpoint_step(f, args, h, y, y_next)
    if solver == SOLVER_CD:
        if f.__name__ == "lorenz":      return cd_step_lorenz(args, h, y, y_next)
        if f.__name__ == "chen":        return cd_step_chen(args, h, y, y_next)
        
        raise ValueError("CD-method is not supported for given function")
    
    raise ValueError("Unknown ODE-solver method")
    

# ================================================================================
def solve_ode(
    f:          RHSFunc,                # input function (right-hand side of the differential equation)
    args:       NDArray[np.float64],    # input function arguments
    num_steps:  int,                    # number of integration steps
    h:          float,                  # step size
    y0:         NDArray[np.float64],    # initial conditions (state vector)
    solver: ODESolver = SOLVER_RK4      # solver
) -> NDArray[np.float64]:

    if solver == SOLVER_CD_LORENZ:      return cd_lorenz(args, num_steps, h, y0)
    if solver == SOLVER_CD_CHEN:        return cd_chen(args, num_steps, h, y0)
    
    if solver == SOLVER_EULER:          return euler(f, args, num_steps, h, y0)
    if solver == SOLVER_EULER_CROMER:   return euler_cromer(f, args, num_steps, h, y0)
    if solver == SOLVER_RK4:            return runge_kutta_4(f, args, num_steps, h, y0)
    if solver == SOLVER_MIDPOINT:       return midpoint(f, args, num_steps, h, y0)
    if solver == SOLVER_CD:
        if f.__name__ == "lorenz":      return cd_lorenz(args, num_steps, h, y0)
        if f.__name__ == "chen":        return cd_chen(args, num_steps, h, y0)
        
        raise ValueError("CD-method is not supported for given function")
    
    raise ValueError(f"Unknown ODE-solver method")

# ================================================================================