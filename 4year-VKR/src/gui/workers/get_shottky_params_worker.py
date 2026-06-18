from PySide6.QtCore import QObject, Signal
import numpy as np

from core.types import AppState
from core.shottky import find_best_schottky_params
from core.algorithms import get_period_indices, get_num_periods

class GetShottkyParamsWorker(QObject):
    params_found = Signal(object)
    param_found = Signal(int)
    error_occurred = Signal(str)
    finished = Signal()

    def __init__(self, app_state: AppState):
        super().__init__()
        self._app_state = app_state

    def _on_param_found(self, i):
        self.param_found.emit(i)

    def run_task(self):
        try:
            start, _ = get_period_indices(self._app_state.V.size, self._app_state.first_cycle_idx, self._app_state.V_zeros, segments_per_period=2, period_start_segment_idx=0)
            _, end = get_period_indices(self._app_state.V.size, self._app_state.last_cycle_idx, self._app_state.V_zeros, segments_per_period=2, period_start_segment_idx=0)
            
            V = self._app_state.V[start : end]; I = self._app_state.I[start : end]
            V_zeros = self._app_state.V_zeros[(self._app_state.V_zeros >= start) & (self._app_state.V_zeros <= end)] - start
            V_maxima = self._app_state.V_maxima[self._app_state.first_cycle_idx : self._app_state.last_cycle_idx + 1] - start
            V_minima = self._app_state.V_minima[self._app_state.first_cycle_idx : self._app_state.last_cycle_idx + 1] - start
            
            n_cycles = get_num_periods(V_zeros, segments_per_period=2)
            params_buffer = np.zeros((n_cycles, 5), dtype=np.float64)
            period_samples = 1 / self._app_state.V_freq / self._app_state.dt

            find_best_schottky_params(
                V, I, V_zeros, V_maxima, V_minima,
                self._app_state.k_set, self._app_state.k_reset,
                period_samples,
                starts_with_hrs=self._app_state.starts_with_hrs,
                params_buffer=params_buffer,
                progress_callback=self._on_param_found
            )

            self.params_found.emit(params_buffer)

        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.finished.emit()