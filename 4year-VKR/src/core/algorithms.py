import numpy as np
from scipy.ndimage import median_filter
from scipy.signal import savgol_filter

# ==============================================================================

def find_zeros(signal: np.ndarray) -> np.ndarray:
    signal = np.asarray(signal)

    if signal.ndim != 1:
        raise ValueError("signal must be 1-dimensional")

    if signal.size < 2:
        return np.array([], dtype=int)

    left = signal[:-1]
    right = signal[1:]

    crosses = (
        (left == 0)
        | (right == 0)
        | ((left < 0) & (right > 0))
        | ((left > 0) & (right < 0))
    )

    if not np.any(crosses):
        return np.array([], dtype=int)

    idxs = np.flatnonzero(crosses)

    chosen = np.where(
        np.abs(left[idxs]) <= np.abs(right[idxs]),
        idxs,
        idxs + 1,
    )

    mask = np.concatenate(([True], chosen[1:] != chosen[:-1]))

    return chosen[mask].astype(int)

# ==============================================================================

def _filter_zero_candidates(
    zero_idxs: np.ndarray,
    min_distance: int,
) -> np.ndarray:
    zero_idxs = np.asarray(zero_idxs, dtype=int)

    if min_distance < 1:
        raise ValueError("min_distance must be positive")

    if zero_idxs.size == 0:
        return np.array([], dtype=int)

    groups = np.split(
        zero_idxs,
        np.flatnonzero(np.diff(zero_idxs) >= min_distance) + 1,
    )

    result = [
        group[(group.size - 1) // 2]
        for group in groups
    ]

    return np.array(result, dtype=int)

# ==============================================================================

def find_stable_zeros(
    signal: np.ndarray,
    *,
    min_distance: int,
) -> np.ndarray:
    zero_idxs = find_zeros(signal)

    return _filter_zero_candidates(
        zero_idxs,
        min_distance=min_distance,
    )

# ==============================================================================

def find_extrema(
    signal: np.ndarray,
    *,
    smooth: bool = True,
    smooth_window: int | None = None,
    smooth_mode: str = "wrap",
) -> tuple[int, int]:
    signal = np.asarray(signal)
    smooth_window = (smooth_window) if (smooth_window % 2 != 0) else (smooth_window + 1)
    smooth_window = min(5, max(smooth_window, signal.size))

    if signal.size == 0:
        raise ValueError("signal must not be empty")
    if not smooth:
        return int(np.argmin(signal)), int(np.argmax(signal))

    smoothed = savgol_filter(signal, window_length=smooth_window, polyorder=3, mode=smooth_mode)

    return int(np.argmin(smoothed)), int(np.argmax(smoothed))

# ==============================================================================

def estimate_frequency_fft(
    signal: np.ndarray,
    dt: float,
    min_rel_amp: float = 0.3,
) -> float:
    if signal.ndim != 1:
        raise ValueError("signal must be 1-dimensional")
    if signal.size < 2:
        raise ValueError("signal must contain at least 2 points")
    if dt <= 0:
        raise ValueError("dt must be positive")
    if not (0 < min_rel_amp <= 1):
        raise ValueError("min_rel_amp must be in range (0, 1]")

    signal_mean = np.mean(signal)

    spectrum = np.fft.rfft(signal - signal_mean)
    amplitudes = np.abs(spectrum)

    amplitudes[0] = 0.0

    max_amp = np.max(amplitudes)
    if max_amp == 0:
        raise ValueError("cannot estimate frequency of a constant signal")

    strong = amplitudes >= min_rel_amp * max_amp

    idxs = np.flatnonzero(strong)
    if idxs.size == 0:
        raise ValueError("no significant frequency component found")

    idx = idxs[0]

    return float(idx / (signal.size * dt))
    # freqs = np.fft.rfftfreq(signal.size, d=dt)
    # return float(freqs[idx])

# ==============================================================================

def get_num_cycles(n_points, zero_indices, peak_indices, valley_indices):
    excess_zero_on_start = zero_indices[0] < valley_indices[0] < zero_indices[1]
    excess_zero_on_end = zero_indices[-2] < peak_indices[-1] < zero_indices[-1]
    excess_zeros = int(excess_zero_on_start) + int(excess_zero_on_end)
    
    incomplete_on_start = (zero_indices[0] > 0) or (excess_zero_on_start)
    incomplete_on_end = (zero_indices[-1] < n_points - 1) or (excess_zero_on_end)

    complete_cycles = (len(zero_indices) - excess_zeros) // 2
    return complete_cycles + int(incomplete_on_start) + int(incomplete_on_end)

def get_num_periods(zero_indices, segments_per_period=2):
    if len(zero_indices) == 0:
        return 0
    if (len(zero_indices) + segments_per_period) % 2 == 0:
        return 1 + (len(zero_indices) - 1) // segments_per_period
    else:
        return (len(zero_indices) - 1) // segments_per_period

# ==============================================================================

def get_valid_cycle_bounds(n_points, zero_indices, peak_indices, valley_indices):
    if len(zero_indices) < 2:
        return (0, n_points)
    
    excess_zero_on_start = zero_indices[0] < valley_indices[0] < zero_indices[1]
    excess_zero_on_end = zero_indices[-2] < peak_indices[-1] < zero_indices[-1]
    
    valid_start = zero_indices[0 + int(excess_zero_on_start)]
    valid_end = zero_indices[n_points - 1 - int(excess_zero_on_end)] + 1

    return (valid_start, valid_end)

# ==============================================================================

# Извлекает индексы начала и конца i-го периода внутри периодического сигнала 
def get_period_indices(n_signal_points: int, i: int, zero_indices: np.ndarray, segments_per_period: int = 2, period_start_segment_idx: int = 0):
    if (i < 0) or (segments_per_period < 1) or (period_start_segment_idx < 0):
        return (-1, -1)
    if len(zero_indices) == 0:
        return (0, n_signal_points)
    
    # normalize
    period_start_segment_idx %= segments_per_period

    if period_start_segment_idx >= len(zero_indices):
        return (0, n_signal_points) if i == 0 else (-1, -1)

    incomplete_on_start = 1 if zero_indices[0 + period_start_segment_idx] != 0 else 0
    p_start, p_end = i * segments_per_period, (i + 1) * segments_per_period

    p_start += period_start_segment_idx
    p_end += period_start_segment_idx
    
    start_zero_idx = p_start - incomplete_on_start * segments_per_period
    end_zero_idx = p_end - incomplete_on_start * segments_per_period

    if start_zero_idx >= len(zero_indices):
        return (-1, -1)

    start   = (zero_indices[start_zero_idx]) if (start_zero_idx >= 0) else (0)
    end     = (zero_indices[end_zero_idx]) if (end_zero_idx < len(zero_indices)) else (n_signal_points)
        
    return start, end

# ==============================================================================

def detect_breakpoint(
    y: np.ndarray,
    min_seg_len: int = 5,
    weights=(0.5, 0.5),
    x: np.ndarray = None
):
    # Кусочно-линейная аппроксимация с оптимизацией точки излома.
    # Минимизирует RSS двух прямых.
    
    n_points = len(y)
    
    valid_range = range(min_seg_len, n_points - min_seg_len + 1)
    best_k, best_rss = None, np.inf
    
    for k in valid_range:
        y1 = y[:k]
        y2 = y[k:]
        
        # Линейная аппроксимация по индексу (равномерная дискретизация)
        x1 = x[:k] if (x is not None) else np.arange(len(y1))
        x2 = x[k:] if (x is not None) else np.arange(len(y2))
        m1, c1 = np.polyfit(x1, y1, 1)
        m2, c2 = np.polyfit(x2, y2, 1)
        
        rss1 = np.sum((y1 - (m1*x1 + c1))**2)
        rss2 = np.sum((y2 - (m2*x2 + c2))**2)

        rss = weights[0] * rss1 + weights[1] * rss2

        # rss = np.sum((y1 - (m1*x1 + c1))**2) + np.sum((y2 - (m2*x2 + c2))**2)
        # rss = np.sum(np.abs(y1 - (m1*x1 + c1))) + np.sum(np.abs(y2 - (m2*x2 + c2)))
        
        if rss < best_rss:
            best_rss = rss
            best_k = k
    
    return best_k, best_rss

# ==================================================================================================

def detect_breakpoint_fast(
    y: np.ndarray,
    min_seg_len: int = 3,
    weights=(0.5, 0.5),
    x: np.ndarray = None
):
    n_points = len(y)
    
    # Если x не задан — используем равномерную сетку
    if x is None:
        x = np.arange(n_points)
    
    # Кумулятивные суммы для O(1) вычисления статистик сегментов
    cum_y = np.concatenate(([0], np.cumsum(y)))
    cum_y2 = np.concatenate(([0], np.cumsum(y**2)))
    cum_x = np.concatenate(([0], np.cumsum(x)))
    cum_x2 = np.concatenate(([0], np.cumsum(x**2)))
    cum_xy = np.concatenate(([0], np.cumsum(x * y)))

    # Закрытая формула RSS для линейной регрессии
    def _calc_rss(n, Sx, Sxx, Sy, Syy, Sxy):
        denom = n * Sxx - Sx**2
        if denom == 0: 
            return np.inf
        m = (n * Sxy - Sx * Sy) / denom
        c = (Sy - m * Sx) / n
        return max(0.0, Syy - 2*m*Sxy - 2*c*Sy + m**2*Sxx + 2*m*c*Sx + n*c**2)

    def _calc_total_rss(k):
        # Сегмент 1: [0, k)
        n1 = k
        Sx1 = cum_x[k] - cum_x[0]
        Sxx1 = cum_x2[k] - cum_x2[0]
        Sy1 = cum_y[k] - cum_y[0]
        Syy1 = cum_y2[k] - cum_y2[0]
        Sxy1 = cum_xy[k] - cum_xy[0]
        rss1 = _calc_rss(n1, Sx1, Sxx1, Sy1, Syy1, Sxy1)
        
        # Сегмент 2: [k, n_points)
        n2 = n_points - k
        Sx2 = cum_x[-1] - cum_x[k]
        Sxx2 = cum_x2[-1] - cum_x2[k]
        Sy2 = cum_y[-1] - cum_y[k]
        Syy2 = cum_y2[-1] - cum_y2[k]
        Sxy2 = cum_xy[-1] - cum_xy[k]
        rss2 = _calc_rss(n2, Sx2, Sxx2, Sy2, Syy2, Sxy2)
        
        return weights[0] * rss1 + weights[1] * rss2

    def _calc_grad(k, rss):
        if k + 1 >= n_points - min_seg_len:
            return 0
        rss2 = _calc_total_rss(k + 1)
        return rss2 - rss

    valid_range = range(min_seg_len, n_points - min_seg_len + 1)
    if len(valid_range) < 2:
        return min_seg_len, np.inf

    # Бинарный поиск точки излома
    k = -1
    k_prev = -3
    left = valid_range[0]
    right = valid_range[-1]

    while np.abs(k - k_prev) > 1:
        k_prev = k
        k = (left + right) // 2
        rss = _calc_total_rss(k)
        grad = _calc_grad(k, rss)

        if grad < 0:
            left = k
        else:
            right = k

    best_k = k
    best_rss = _calc_total_rss(best_k)
    return best_k, best_rss

# ==================================================================================================

def interpolate_break_median(signal, break_index, window_size):
    interval_start = int(max(0, break_index - window_size // 2))
    interval_end = int(min(len(signal) - 1, break_index + window_size // 2) + 1)

    left = max(0, interval_start - window_size // 2)
    right = min(interval_end + window_size // 2, len(signal))

    processed = median_filter(signal[left : right], size=window_size, mode='wrap')
    
    signal[interval_start : interval_end] = processed[interval_start - left : len(processed) - (right - interval_end)]

# ==================================================================================================

def interpolate_break_with_line(signal, break_index, break_width, mode='mirror'):
    if break_width % 2 == 0 or break_width < 3:
        raise ValueError("break_width should be odd and > 1")
    assert mode in ['mirror', 'wrap'], "Incorrect mode was given"

    break_width = min(break_width, len(signal))

    left = max(0, break_index - break_width // 2)
    right = min(break_index + break_width // 2, len(signal) - 1)

    left_out = break_index - break_width // 2 < 0
    right_out = break_index + break_width // 2 >= len(signal)

    x1 = left
    x2 = right
    if left_out:
        x1 = (len(signal) - break_width // 2 - break_index) if (mode == 'wrap') else (break_width // 2 - break_index)
    if right_out:
        x2 = (break_width // 2 - break_index) if (mode == 'wrap') else (len(signal) - break_width // 2 - break_index)

    x1 = int(x1)
    x2 = int(x2)
    y1 = signal[x1]
    y2 = signal[x2]
    k = (y2 - y1) / (break_width)

    left_offset = (break_width // 2 - break_index) if (left_out) else (0)
    width = right - left + 1
    signal[left : right + 1] = y1 + k * np.linspace(left_offset, left_offset + width, width)

# ==================================================================================================

def fit_by_center_window(V_part, I_part, center_idx, frac=0.2):
    n = len(V_part)
    half_window = max(2, int(frac * n / 2))

    left = max(0, center_idx - half_window)
    right = min(n, center_idx + half_window + 1)

    if right - left < 2:
        return np.polyfit(V_part, I_part, 1)

    return np.polyfit(V_part[left:right], I_part[left:right], 1)

# ==================================================================================================