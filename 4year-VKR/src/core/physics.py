import numpy as np

# ==============================================================================

def calculate_R(V, I):
    R = np.empty_like(V)
    np.divide(V, I, out=R, where=(I != 0))
    R[I == 0] = np.inf
    return R

# ==============================================================================

def calculate_G(V, I):
    G = np.empty_like(V)
    np.divide(I, V, out=G, where=(V != 0))
    G[V == 0] = np.inf
    return G