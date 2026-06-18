import numpy as np
from scipy.optimize import differential_evolution

from core.memristor import extract_schottky_current, extract_memristive_current, get_on_index, get_off_index
from core.algorithms import get_period_indices, get_num_periods, fit_by_center_window
from core.memristor import detect_set, detect_reset
from core.filter import filter_current

# ==============================================================================

# def find_best_shottky_target(params, V, I, V_max_idx, V0_idx, V_min_idx, set_index, reset_index, starts_with_hrs=False):
#     phi, a_f, a_r, b_f, b_r = params
    
#     I_s = extract_schottky_current(V, a_f, a_r, b_f, b_r)
#     I_m = extract_memristive_current(I, phi, I_s)

#     on_index = get_on_index(V_max_idx, V_min_idx, starts_with_hrs=starts_with_hrs)
#     off_index = get_off_index(V_max_idx, V_min_idx, starts_with_hrs=starts_with_hrs)

#     # get HRS area
#     if starts_with_hrs:
#         I_m_HRS = np.concatenate([I_m[off_index : ], I_m[ : set_index]], axis=0)
#         I_HRS = np.concatenate([I[off_index : ], I[ : set_index]], axis=0)
#         V_HRS = np.concatenate([V[off_index : ], V[ : set_index]], axis=0)
#     else:
#         I_m_HRS = I_m[off_index : set_index]
#         I_HRS = I[off_index : set_index]
#         V_HRS = V[off_index : set_index]
    
#     # get LRS area
#     if starts_with_hrs:
#         I_m_LRS = I_m[on_index : reset_index]
#         V_LRS = V[on_index : reset_index]
#     else:
#         I_m_LRS = np.concatenate([I_m[on_index : ], I_m[ : reset_index]], axis=0)
#         V_LRS = np.concatenate([V[on_index : ], V[ : reset_index]], axis=0)

#     # настройка для более сильного контроля за краями LRS / HRS
#     lrs_center = (V0_idx - reset_index) if (starts_with_hrs) else (len(V) - on_index)
#     hrs_center = (len(V) - off_index) if (starts_with_hrs) else (V0_idx - off_index)
#     hrs_center = max(1, hrs_center)
#     lrs_center = max(1, lrs_center)

#     # Во сколько раз штраф на краях больше, чем в центре (в `edge_multiplier + 1` раз)
#     hrs_edge_multiplier = 3.0
#     lrs_edge_multiplier = 3.0

#     # calculate RSS(HRS) — RSS of HRS-curve
#     x1 = V_HRS
#     idxs1 = np.arange(len(V_HRS))
#     # dist_from_center = np.abs(idxs1 - hrs_center) / hrs_center
#     # weights_hrs = -1.0 + hrs_edge_multiplier * np.exp(dist_from_center)
#     # m1, c1 = fit_by_center_window(V_HRS, I_HRS, hrs_center, frac=0.3)
#     # rss_hrs = np.sum(weights_hrs * (I_m_HRS - (m1*x1 + c1))**2) / np.sum(weights_hrs)
#     weights_hrs = np.ones(len(V_HRS))
#     left_mask = idxs1 <= hrs_center
#     right_mask = idxs1 > hrs_center
#     # левая часть: экспоненциальный рост штрафа к краю
#     dist_left = (hrs_center - idxs1[left_mask]) / hrs_center
#     weights_hrs[left_mask] = 1.0 + hrs_edge_multiplier * (np.exp(dist_left) - 1.0)
#     # правая часть: линейный рост штрафа от центра к правому краю
#     right_len = max(1, len(V_HRS) - 1 - hrs_center)
#     dist_right = (idxs1[right_mask] - hrs_center) / right_len
#     weights_hrs[right_mask] = 1.0 + hrs_edge_multiplier * dist_right
#     m1, c1 = fit_by_center_window(V_HRS, I_HRS, hrs_center, frac=1.0)
#     rss_hrs = np.mean((I_m_HRS - (m1*x1 + c1))**2)
#     # rss_hrs = np.sum(weights_hrs * (I_m_HRS - (m1*x1 + c1))**2) / np.sum(weights_hrs)

#     # calculate RSS(LRS) — RSS of LRS-curve
#     x2 = V_LRS
#     idxs2 = np.arange(len(V_LRS))
#     dist_from_center = np.abs(idxs2 - lrs_center) / lrs_center
#     weights_lrs = -1.0 + lrs_edge_multiplier * np.exp(dist_from_center)
#     m2, c2 = np.polyfit(x2, I_m_LRS, 1, w=np.sqrt(weights_lrs))
#     rss_lrs = np.sum(weights_lrs * (I_m_LRS - (m2*x2 + c2))**2) / np.sum(weights_lrs)

#     intercept_violation = c1**2 + c2**2

#     hrs_weight = 1.0
#     lrs_weight = 1.0

#     return (
#         hrs_weight * rss_hrs + lrs_weight * rss_lrs
#         + 1e1 * intercept_violation
#     )

# def find_best_shottky_target(params, V, I, V_max_idx, V0_idx, V_min_idx, set_index, reset_index, starts_with_hrs=False):
#     phi, a_f, a_r, b_f, b_r = params
    
#     I_s = extract_schottky_current(V, a_f, a_r, b_f, b_r)
#     I_m = extract_memristive_current(I, phi, I_s)

#     on_index = get_on_index(V_max_idx, V_min_idx, starts_with_hrs=starts_with_hrs)
#     off_index = get_off_index(V_max_idx, V_min_idx, starts_with_hrs=starts_with_hrs)

#     # get HRS area
#     if starts_with_hrs:
#         I_m_HRS = np.concatenate([I_m[off_index : ], I_m[ : set_index]], axis=0)
#         I_HRS = np.concatenate([I[off_index : ], I[ : set_index]], axis=0)
#         V_HRS = np.concatenate([V[off_index : ], V[ : set_index]], axis=0)
#     else:
#         I_m_HRS = I_m[off_index : set_index]
#         I_HRS = I[off_index : set_index]
#         V_HRS = V[off_index : set_index]
    
#     # get LRS area
#     if starts_with_hrs:
#         I_m_LRS = I_m[on_index : reset_index]
#         V_LRS = V[on_index : reset_index]
#     else:
#         I_m_LRS = np.concatenate([I_m[on_index : ], I_m[ : reset_index]], axis=0)
#         V_LRS = np.concatenate([V[on_index : ], V[ : reset_index]], axis=0)

#     # настройка для более сильного контроля за краями LRS / HRS
#     lrs_center = (V0_idx - reset_index) if (starts_with_hrs) else (len(V) - on_index)
#     hrs_center = (len(V) - off_index) if (starts_with_hrs) else (V0_idx - off_index)
#     hrs_center = max(1, hrs_center)
#     lrs_center = max(1, lrs_center)

#     # Во сколько раз штраф на краях больше, чем в центре (в `edge_multiplier + 1` раз)
#     hrs_edge_multiplier = 3.0
#     lrs_edge_multiplier = 3.0

#     # calculate RSS(HRS) — RSS of HRS-curve
#     x1 = V_HRS
#     idxs1 = np.arange(len(V_HRS))
#     dist_from_center = np.abs(idxs1 - hrs_center) / hrs_center
#     weights_hrs = -1.0 + hrs_edge_multiplier * np.exp(dist_from_center)
#     # m1, c1 = fit_by_center_window(V_HRS, I_m_HRS, hrs_center, frac=0.3)
#     m1, c1 = np.polyfit(x1, I_m_HRS, 1, w=np.sqrt(weights_hrs))
#     rss_hrs = np.sum(weights_hrs * (I_m_HRS - (m1*x1 + c1))**2) / np.sum(weights_hrs)

#     # calculate RSS(LRS) — RSS of LRS-curve
#     x2 = V_LRS
#     idxs2 = np.arange(len(V_LRS))
#     dist_from_center = np.abs(idxs2 - lrs_center) / lrs_center
#     weights_lrs = -1.0 + lrs_edge_multiplier * np.exp(dist_from_center)
#     m2, c2 = np.polyfit(x2, I_m_LRS, 1, w=np.sqrt(weights_lrs))
#     rss_lrs = np.sum(weights_lrs * (I_m_LRS - (m2*x2 + c2))**2) / np.sum(weights_lrs)

#     m_ref, c_ref = fit_by_center_window(V_HRS, I_HRS, hrs_center, frac=0.3)
#     # I_ref_HRS = m_ref * V_HRS + c_ref
    
#     intercept_violation = c1**2 + c2**2
#     hrs_slope_violation = max(0.0, m_ref / 10 - m1) ** 2

#     hrs_weight = 1.0
#     lrs_weight = 1.0

#     # trajectory_violation = np.mean(np.abs(I_m_HRS - I_ref_HRS))

#     return (
#         hrs_weight * rss_hrs + lrs_weight * rss_lrs
#         + 1e1 * intercept_violation
#         + 1e1 * hrs_slope_violation
#         # + 0.1e0 * trajectory_violation
#     )

def find_best_shottky_target(params, V, I, V_max_idx, V0_idx, V_min_idx, set_index, reset_index, starts_with_hrs=False):
    phi, a_f, a_r, b_f, b_r = params
    
    I_s = extract_schottky_current(V, a_f, a_r, b_f, b_r)
    I_m = extract_memristive_current(I, phi, I_s)

    on_index = get_on_index(V_max_idx, V_min_idx, starts_with_hrs=starts_with_hrs)
    off_index = get_off_index(V_max_idx, V_min_idx, starts_with_hrs=starts_with_hrs)

    # get HRS area
    if starts_with_hrs:
        I_m_HRS = np.concatenate([I_m[off_index : ], I_m[ : set_index]], axis=0)
        V_HRS = np.concatenate([V[off_index : ], V[ : set_index]], axis=0)
    else:
        I_m_HRS = I_m[off_index : set_index]
        V_HRS = V[off_index : set_index]
    
    # get LRS area
    if starts_with_hrs:
        I_m_LRS = I_m[on_index : reset_index]
        V_LRS = V[on_index : reset_index]
    else:
        I_m_LRS = np.concatenate([I_m[on_index : ], I_m[ : reset_index]], axis=0)
        V_LRS = np.concatenate([V[on_index : ], V[ : reset_index]], axis=0)

    def fit_zero_intercept_line(V_part, I_part):
        if len(V_part) < 2:
            return 0.0, np.inf

        denom = np.sum(V_part**2)

        if denom <= 0:
            return 0.0, np.inf

        m = np.sum(V_part * I_part) / denom
        I_fit = m * V_part

        mse = np.mean((I_part - I_fit) ** 2)

        # Нормировка нужна, чтобы целевая функция меньше зависела
        # от абсолютного масштаба тока
        scale = np.mean(I_part**2) + 1e-30
        residual = mse / scale

        return m, residual

    m_hrs, hrs_linearity = fit_zero_intercept_line(V_HRS, I_m_HRS)
    m_lrs, lrs_linearity = fit_zero_intercept_line(V_LRS, I_m_LRS)

    # Штраф за отрицательный наклон HRS.
    # Если m_hrs >= 0, штраф равен нулю.
    # Если m_hrs < 0, штраф растет квадратично.
    V_scale = np.max(np.abs(V)) + 1e-30
    I_scale = np.max(np.abs(I)) + 1e-30
    slope_scale = I_scale / V_scale

    hrs_negative_slope_penalty = (max(0.0, -m_hrs) / slope_scale) ** 2

    hrs_weight = 1.0
    lrs_weight = 1.0
    slope_weight = 10.0

    target = (
        hrs_weight * hrs_linearity
        + lrs_weight * lrs_linearity
        + slope_weight * hrs_negative_slope_penalty
    )

    return target

# ==============================================================================

def find_best_schottky_params_step(param_bounds, V, I, V_max_idx, V0_idx, V_min_idx, set_index, reset_index, starts_with_hrs=False, maxiter=500, init_population=None, seed=42):
    if init_population is not None:
        result = differential_evolution(
            func=find_best_shottky_target,
            bounds=param_bounds,
            args=(V, I, V_max_idx, V0_idx, V_min_idx, set_index, reset_index, starts_with_hrs),
            seed=seed,
            maxiter=maxiter,
            init=init_population
            )
    else:
        result = differential_evolution(
            func=find_best_shottky_target,
            bounds=param_bounds,
            args=(V, I, V_max_idx, V0_idx, V_min_idx, set_index, reset_index, starts_with_hrs),
            seed=seed,
            maxiter=maxiter
            )
    
    return result.x, result.population

# ==============================================================================

def find_best_schottky_params(V, I, V_zeros, V_maxima, V_minima, k_set, k_reset, period_samples, starts_with_hrs=False, progress_callback=None, params_buffer=None):
    # оптимальные границы параметров для нормализованного тока и напряжения
    param_bounds = [
        (0.95, 0.99),
        (1e-3, 1e2),
        (1e-3, 1e2),
        (0, 30),
        (0, 30),
    ]
    
    num_cycles = get_num_periods(V_zeros, segments_per_period=2)

    if params_buffer is None:
        params_buffer = np.zeros((num_cycles, 5), dtype=np.float64)

    last_population = []
    for j in range(num_cycles):
        start, end = get_period_indices(len(V), j, V_zeros, segments_per_period=2, period_start_segment_idx=0)

        if start == -1 or end == -1:
            if progress_callback: progress_callback(j + 1)
            continue

        # j-й цикл ВАХ-ки
        i = I[start : end]; v = V[start : end]
            
        # Находим нули и экстремумы
        v_zeros = V_zeros[(V_zeros >= start) & (V_zeros <= end)] - start
        if len(v_zeros) != 3:
            if progress_callback: progress_callback(j + 1)
            continue

        V0_idx = v_zeros[1]
        V_max_idx = V_maxima[j] - start
        V_min_idx = V_minima[j] - start

        # Нормализация
        i_abs_max = np.max(np.abs(i))
        i_normalized = i / i_abs_max
        v_abs_max = np.max([v[V_max_idx], v[V_min_idx]])
        v_normalized = v / v_abs_max

        i_smoothed = filter_current(i, period_samples, high_smooth=True, mode='wrap')

        on_index = get_on_index(V_max_idx, V_min_idx, starts_with_hrs=starts_with_hrs)
        off_index = get_off_index(V_max_idx, V_min_idx, starts_with_hrs=starts_with_hrs)

        set_index = detect_set(v, i_smoothed, on_index, V0_idx, k=k_set, starts_with_hrs=starts_with_hrs)
        reset_index = detect_reset(v, i_smoothed, off_index, V0_idx, k=k_reset, starts_with_hrs=starts_with_hrs)

        # оптимизация
        params, last_population = find_best_schottky_params_step(param_bounds,
            v_normalized, i_normalized, V_max_idx, V0_idx, V_min_idx, set_index, reset_index, 
            maxiter=500, init_population=(last_population) if (j > 0) else (None))
        
        # обратная нормализация
        params[1 : 3] *= i_abs_max
        params[3 : 5] /= v_abs_max

        params_buffer[j] = params

        if progress_callback:
            progress_callback(j + 1)

    return params_buffer

# ==============================================================================