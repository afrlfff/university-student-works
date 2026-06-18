from scipy.signal import savgol_filter

def filter_current(I, period_samples, high_smooth=True, mode='wrap'):
    high_smooth_window = int(round(period_samples * (101 / 5200)))
    soft_smooth_window = int(round(period_samples * (31 / 5200)))

    high_smooth_window += int(high_smooth_window % 2 == 0)
    soft_smooth_window += int(soft_smooth_window % 2 == 0)

    if high_smooth:
        window = min(len(I) - int(len(I) % 2 == 0), high_smooth_window)
        return savgol_filter(I, window_length=window, polyorder=3, mode=mode)
    else:
        window = min(len(I) - int(len(I) % 2 == 0), soft_smooth_window)
        return savgol_filter(I, window_length=window, polyorder=3, mode=mode)
    
def filter_conductivity(G, period_samples, high_smooth=True, mode='wrap'):
    high_smooth_window = int(round(period_samples * (201 / 5200)))
    soft_smooth_window = int(round(period_samples * (61 / 5200)))
    
    high_smooth_window += int(high_smooth_window % 2 == 0)
    soft_smooth_window += int(soft_smooth_window % 2 == 0)

    if high_smooth:
        window = min(len(G) - int(len(G) % 2 == 0), high_smooth_window)
        return savgol_filter(G, window_length=window, polyorder=3, mode=mode)
    else:
        window = min(len(G) - int(len(G) % 2 == 0), soft_smooth_window)
        return savgol_filter(G, window_length=window, polyorder=3, mode=mode)