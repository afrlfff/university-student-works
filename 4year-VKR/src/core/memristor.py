import numpy as np

from core.algorithms import detect_breakpoint_fast, interpolate_break_with_line, interpolate_break_median
from core.physics import calculate_G
from core.filter import filter_conductivity, filter_current

# ==================================================================================================

def extract_schottky_current(V, a_f, a_r, b_f, b_r):
    return a_f * np.exp(b_f * V) - a_r * np.exp(-b_r * V)

def extract_memristive_current(I, phi, I_s):
    return (I - (1 - phi) * I_s) / phi

# ==================================================================================================

def get_on_index(V_max_idx, V_min_idx, starts_with_hrs=True):
    return (min(V_max_idx, V_min_idx)) if (starts_with_hrs) else (max(V_max_idx, V_min_idx))

def get_off_index(V_max_idx, V_min_idx, starts_with_hrs=True):
    return (max(V_max_idx, V_min_idx)) if (starts_with_hrs) else (min(V_max_idx, V_min_idx))

# ==================================================================================================

def detect_set(V, I, on_index, V0_index, k=1.0, starts_with_hrs=True):
    if starts_with_hrs:
        index, _ = detect_breakpoint_fast(I[0 : on_index + 1], weights=(k, 1.0), x=V[0 : on_index + 1])
        return index
    else:
        index, _ = detect_breakpoint_fast(I[V0_index : on_index + 1], weights=(k, 1.0), x=V[V0_index : on_index + 1])
        return V0_index + index

# ==============================================================================

def detect_reset(V, I, off_index, V0_index, k=1.0, starts_with_hrs=True):
    if starts_with_hrs:
        index, _ = detect_breakpoint_fast(I[V0_index : off_index + 1], weights=(k, 1.0), x=V[V0_index : off_index + 1])
        return V0_index + index
    else:
        index, _ = detect_breakpoint_fast(I[0 : off_index + 1], weights=(k, 1.0), x=V[0 : off_index + 1])
        return index

# ==============================================================================

# def check_start_with_hrs(V, I, V_max_idx, V0_idx, V_min_idx) -> bool:
#     first_segemnt_bounds = (0, V_max_idx if (V_max_idx < V_min_idx) else V_min_idx)
#     third_segemnt_bounds = (V0_idx, V_min_idx if (V_min_idx < V_max_idx) else V_max_idx)

#     k = 0.1

# ==============================================================================

def extract_X_state(G, V_zeros, on_index, off_index, set_index, reset_index, break_length, period_samples, starts_with_hrs=False):
    filter_intervals = [
        (0, (set_index if starts_with_hrs else reset_index)),
        ((on_index if starts_with_hrs else off_index), (reset_index if starts_with_hrs else set_index)),
        ((off_index if starts_with_hrs else on_index), len(G))
        ]

    G_filtered = G.copy()
    for filter_interval in filter_intervals:
        f_start, f_end = filter_interval
        G_filtered[f_start : f_end] = filter_conductivity(G_filtered[f_start : f_end], period_samples, high_smooth=True, mode='mirror')
    for zero_index in V_zeros:
        # interpolate_break_with_line(G_filtered, zero_index, break_length, mode='wrap')
        interpolate_break_median(G_filtered, zero_index, int(break_length) + int((break_length) % 2 == 0))

    # Переменная состояния X
    G_on = np.max(G_filtered); G_off = np.min(G_filtered)
    X = (G_filtered - G_off) / (G_on - G_off + 1e-12)

    return X, G_on, G_off