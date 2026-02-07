from numpy import uint8

# ODE solver type
ODESolver = uint8

SOLVER_EULER        = uint8(1)
SOLVER_EULER_CROMER = uint8(2)
SOLVER_MIDPOINT     = uint8(3)
SOLVER_RK4          = uint8(4)
SOLVER_CD           = uint8(5)

# additional (for call optimization)
SOLVER_CD_LORENZ    = uint8(6)
SOLVER_CD_CHEN      = uint8(7)