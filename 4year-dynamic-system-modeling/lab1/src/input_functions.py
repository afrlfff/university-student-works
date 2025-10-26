import numpy as np

# ================================================================================

def chen(state, parameters):
    x, y, z = state
    a, b, c = parameters

    dx = a*(y - x)
    dy = (c - a)*x - x*z + c*y
    dz = x*y - b*z

    ma = 1e6

    # check overflow just in case
    if (abs(x) > ma) or (abs(y) > ma) or (abs(z) > ma) or \
        (abs(dx) > ma) or (abs(dy) > ma) or (abs(dz) > ma):
        print("Overflow encountered")
        exit(1)

    return np.array([dx, dy, dz], dtype=np.float32)

# ================================================================================

def lorenz(state, parameters):
    x, y, z = state
    sigma, rho, beta = parameters

    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x*y - beta*z

    ma = 1e6

    # check overflow just in case
    if (abs(x) > ma) or (abs(y) > ma) or (abs(z) > ma) or \
        (abs(dx) > ma) or (abs(dy) > ma) or (abs(dz) > ma):
        print("Overflow encountered")
        exit(1)

    return np.array([dx, dy, dz], dtype=np.float32)

# ================================================================================