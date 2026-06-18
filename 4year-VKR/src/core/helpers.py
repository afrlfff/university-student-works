import numpy as np

def build_time_array(start, end, dt, endpoint=True):
    n = int(np.round((end - start) / dt)) + (1 if endpoint else 0)
    return np.linspace(start, end, n, endpoint=endpoint)