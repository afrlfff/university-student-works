from PySide6.QtWidgets import QWidget
from gui.ui_autogen.ui_state_X_panel import Ui_StateXPanel

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from gui.panels.base_panel import BasePanel
from core.types import AppState
from core.algorithms import get_period_indices
from core.plot import set_scientific_xaxis, set_scientific_yaxis
from core.memristor import extract_schottky_current, extract_memristive_current, extract_X_state, detect_set, detect_reset, get_on_index, get_off_index
from core.helpers import build_time_array
from core.physics import calculate_G
from core.filter import filter_current

class StateXPanel(BasePanel):
    def __init__(self, parent=None, app_state: AppState = None):
        super().__init__(parent, app_state)
        self.ui = Ui_StateXPanel()
        self.ui.setupUi(self)

        self._setup_plot()
        self._connect_signals()
        self.sync()

    def sync(self):
        self._update_controls()
        self.update_plot()

    def update_plot(self):
        if not(self._app_state.is_source_data_valid() and self._app_state.shottky_params.size > 0):
            return

        # подготовка данных
        i = self.ui.spin_cycle.value() - 1 - self._app_state.first_cycle_idx
        phi, a_f, a_r, b_f, b_r = self._app_state.shottky_params[i]

        dt = self._app_state.dt
        period_samples = int(round(1 / self._app_state.V_freq / self._app_state.dt))

        j = self.ui.spin_cycle.value() - 1
        start, end = get_period_indices(self._app_state.V.size, j, self._app_state.V_zeros, segments_per_period=2, period_start_segment_idx=0)
        T = build_time_array(start*dt, (end - 1)*dt, dt, endpoint=True)
        V = self._app_state.V[start : end]
        I = self._app_state.I[start : end]
        I_s = extract_schottky_current(V, a_f, a_r, b_f, b_r)
        I_m = extract_memristive_current(I, phi, I_s)
    
        V_zeros = self._app_state.V_zeros[(self._app_state.V_zeros >= start) & (self._app_state.V_zeros <= end)] - start
        V_max_idx = self._app_state.V_maxima[j] - start
        V_min_idx = self._app_state.V_minima[j] - start
        V0_idx = V_zeros[1]

        I_m_smoothed = filter_current(I_m, period_samples, high_smooth=True, mode='wrap')
        on_index = get_on_index(V_max_idx, V_min_idx, starts_with_hrs=self._app_state.starts_with_hrs)
        off_index = get_off_index(V_max_idx, V_min_idx, starts_with_hrs=self._app_state.starts_with_hrs)
        set_index = detect_set(V, I_m_smoothed, on_index, V0_idx, k=self._app_state.k_set, starts_with_hrs=self._app_state.starts_with_hrs)
        reset_index = detect_reset(V, I_m_smoothed, off_index, V0_idx, k=self._app_state.k_reset, starts_with_hrs=self._app_state.starts_with_hrs)

        # Вычисление
        G = calculate_G(V, I_m)
        X, G_on, G_off = extract_X_state(G, V_zeros, on_index, off_index, set_index, reset_index, 
                                         self._app_state.g_break_length, period_samples, starts_with_hrs=self._app_state.starts_with_hrs)
        dX = np.gradient(X)

        # Обновление кривых
        self._line_G.set_data(T, G)
        self._line_X.set_data(T, X)
        self._line_dX.set_data(T, dX)
        
        self._ax_G.set_ylim(G_off - 0.15 * (G_on - G_off), G_on + 0.15 * (G_on - G_off))

        for ax in (self._ax_G, self._ax_X, self._ax_dX):
            ax.set_xlim(T[0], T[-1])
            ax.relim()
            ax.autoscale_view()
        self._canvas.draw_idle()

    def _connect_signals(self):
        self.ui.slider_cycle.valueChanged.connect(self.ui.spin_cycle.setValue)
        self.ui.spin_cycle.valueChanged.connect(self.ui.slider_cycle.setValue)
        self.ui.spin_cycle.valueChanged.connect(self.update_plot)

    def _update_controls(self):
        app_state_valid = self._app_state.is_source_data_valid()
        
        first_cycle_idx = (self._app_state.first_cycle_idx) if app_state_valid else 0
        last_cycle_idx = (self._app_state.last_cycle_idx) if app_state_valid else 0

        first_cycle_idx_prev = self.ui.spin_cycle.minimum() - 1
        last_cycle_idx_prev = self.ui.spin_cycle.maximum() - 1

        # update ranges
        for w in (self.ui.spin_cycle, self.ui.slider_cycle):
            w.setMinimum(first_cycle_idx + 1)
            w.setMaximum(last_cycle_idx + 1)
        self.ui.lbl_cycle_min.setText(str(first_cycle_idx + 1))
        self.ui.lbl_cycle_max.setText(str(last_cycle_idx + 1))

        # update initial values
        if (first_cycle_idx != first_cycle_idx_prev) or (last_cycle_idx != last_cycle_idx_prev):
            self.ui.spin_cycle.setValue(1)

    def _setup_plot(self):
        self._canvas = FigureCanvas(Figure(figsize=(5, 3), dpi=100, constrained_layout=True))
        self._ax_G = self._canvas.figure.add_subplot(3, 1, 1)
        self._ax_X = self._canvas.figure.add_subplot(3, 1, 2, sharex=self._ax_G)
        self._ax_dX = self._canvas.figure.add_subplot(3, 1, 3, sharex=self._ax_G)
        self._line_G, = self._ax_G.plot([])
        self._line_X, = self._ax_X.plot([])
        self._line_dX, = self._ax_dX.plot([])

        self.ui.mpl_canvas.layout().addWidget(self._canvas)

        for ax in (self._ax_G, self._ax_X, self._ax_dX):
            ax.grid(True, alpha=0.3, linestyle='--')
        self._ax_G.set_ylabel(self.tr("Проводимость, [См]"))
        self._ax_X.set_ylabel("X")
        self._ax_dX.set_ylabel("dX/dt")
        self._ax_dX.set_xlabel(self.tr("Время, [с]"))
        set_scientific_xaxis(self._ax_G)
        set_scientific_yaxis(self._ax_G)