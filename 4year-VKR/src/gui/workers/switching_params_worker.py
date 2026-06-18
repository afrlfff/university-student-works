from PySide6.QtCore import QObject, Signal, QThread

import numpy as np
from core.types import AppState
from core.algorithms import get_period_indices, get_num_periods
from core.physics import calculate_G
from core.memristor import extract_schottky_current, extract_memristive_current, extract_X_state, detect_set, detect_reset, get_on_index, get_off_index
from core.filter import filter_current

class SwitchingParamsWorker(QObject):
    iteration_finished = Signal(int)
    error_occurred = Signal(str)
    data_ready = Signal(np.ndarray, np.ndarray, np.ndarray, np.ndarray)
    finished = Signal()

    def __init__(self, app_state : AppState):
        super().__init__()
        self._app_state = app_state

    def _on_iteration_finished(self, i):
        self.iteration_finished.emit(i)

    def run_task(self):
        try:
            start, _ = get_period_indices(self._app_state.V.size, self._app_state.first_cycle_idx, self._app_state.V_zeros, segments_per_period=2, period_start_segment_idx=0)
            _, end = get_period_indices(self._app_state.V.size, self._app_state.last_cycle_idx, self._app_state.V_zeros, segments_per_period=2, period_start_segment_idx=0)
            
            V = self._app_state.V[start : end]; I = self._app_state.I[start : end]
            V_zeros = self._app_state.V_zeros[(self._app_state.V_zeros >= start) & (self._app_state.V_zeros <= end)] - start
            V_minima = self._app_state.V_minima[self._app_state.first_cycle_idx : self._app_state.last_cycle_idx + 1] - start
            V_maxima = self._app_state.V_maxima[self._app_state.first_cycle_idx : self._app_state.last_cycle_idx + 1] - start
            n_cycles = get_num_periods(V_zeros, segments_per_period=2)
            period_samples = 1 / self._app_state.V_freq / self._app_state.dt

            R_ON    = np.zeros(n_cycles, dtype=np.float64)
            R_OFF   = np.zeros(n_cycles, dtype=np.float64)
            V_SET     = np.zeros(n_cycles, dtype=np.float64)
            V_RESET   = np.zeros(n_cycles, dtype=np.float64)

            for j in range(n_cycles):
                start, end = get_period_indices(V.size, j, V_zeros, segments_per_period=2, period_start_segment_idx=0)

                phi, a_f, a_r, b_f, b_r = self._app_state.shottky_params[j]

                # i-й цикл ВАХ-ки
                i = I[start : end]; v = V[start : end]
                i_s = extract_schottky_current(v, a_f, a_r, b_f, b_r)
                i_m = extract_memristive_current(i, phi, i_s)

                v_zeros = V_zeros[(V_zeros >= start) & (V_zeros <= end)] - start
                v_max_idx = V_maxima[j] - start
                v_min_idx = V_minima[j] - start
                v0_idx = v_zeros[1]

                i_m_smoothed = filter_current(i_m, period_samples, high_smooth=True, mode='wrap')
                on_index = get_on_index(v_max_idx, v_min_idx, starts_with_hrs=self._app_state.starts_with_hrs)
                off_index = get_off_index(v_max_idx, v_min_idx, starts_with_hrs=self._app_state.starts_with_hrs)
                set_index = detect_set(v, i_m_smoothed, on_index, v0_idx, k=self._app_state.k_set, starts_with_hrs=self._app_state.starts_with_hrs)
                reset_index = detect_reset(v, i_m_smoothed, off_index, v0_idx, k=self._app_state.k_reset, starts_with_hrs=self._app_state.starts_with_hrs)


                # Проводимость
                g = calculate_G(v, i_m)
                _, g_on, g_off = extract_X_state(g, v_zeros, on_index, off_index, set_index, reset_index, self._app_state.g_break_length,
                                                period_samples, starts_with_hrs=self._app_state.starts_with_hrs)

                R_ON[j] = 1 / g_on
                R_OFF[j] = 1 / g_off

                V_SET[j] = v[set_index]
                V_RESET[j] = v[reset_index]

                self._on_iteration_finished(j)

            self.data_ready.emit(R_ON, R_OFF, V_SET, V_RESET)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.finished.emit()