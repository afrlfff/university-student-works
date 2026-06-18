from dataclasses import dataclass
from typing import Optional
import numpy as np

from PySide6.QtCore import QSignalBlocker, Signal
from PySide6.QtWidgets import QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from gui.ui_autogen.ui_set_reset_panel import Ui_SetResetPanel

from gui.panels.base_panel import BasePanel
from core.types import AppState
from core.algorithms import get_period_indices, get_num_periods
from core.plot import set_scientific_xaxis, set_scientific_yaxis
from core.memristor import detect_set, detect_reset, get_on_index, get_off_index
from core.filter import filter_current

@dataclass
class SetResetState:
    k_set: float = 1
    k_reset: float = 1


class SetResetPanel(BasePanel):
    data_applied = Signal()
    data_discarded = Signal()

    def __init__(self, parent=None, app_state: AppState = None):
        super().__init__(parent, app_state)
        self.ui = Ui_SetResetPanel()
        self.ui.setupUi(self)

        self._state = SetResetState()

        self._setup_plot()
        self._connect_signals()

        self._write_state_to_ui(self._state)
        self.sync()

    def sync(self):
        self._sync_state_with_app_state()
        self._update_controls()
        self.update_plot()

    def _read_ui_state(self) -> SetResetState:
        return SetResetState(
            k_set= self.ui.spin_k_set.value(),
            k_reset= self.ui.spin_k_reset.value(),
        )

    def _sync_state_with_app_state(self):
        self._state = SetResetState(
            k_set=self._app_state.k_set,
            k_reset=self._app_state.k_reset,
        )
        self._write_state_to_ui(self._state)

    def _write_state_to_ui(self, state: SetResetState):
        with QSignalBlocker(self.ui.spin_k_set), QSignalBlocker(self.ui.spin_k_reset):
            self.ui.spin_k_set.setValue(state.k_set)
            self.ui.spin_k_reset.setValue(state.k_reset)
            self._sync_slider_from_spin(self.ui.slider_k_set, self.ui.spin_k_set, state.k_set)
            self._sync_slider_from_spin(self.ui.slider_k_reset, self.ui.spin_k_reset, state.k_reset)

    def _setup_plot(self):
        self._canvas = FigureCanvas(Figure(figsize=(5, 3), dpi=100, constrained_layout=True))
        self._ax = self._canvas.figure.add_subplot()

        self._line, = self._ax.plot([], [], label=self.tr("ВАХ"))
        self._set_point = self._ax.scatter([], [], label=self.tr("$V_{SET}$"), marker="o", zorder=3, c='C1')
        self._reset_point = self._ax.scatter([], [], label=self.tr("$V_{RESET}$"), marker="o", zorder=3, c='C3')
        self._ax.grid(True, alpha=0.3)
        self._ax.set_xlabel(self.tr("Напряжение, [В]"))
        self._ax.set_ylabel(self.tr("Ток, [А]"))
        set_scientific_xaxis(self._ax); set_scientific_yaxis(self._ax)
        self._ax.legend()

        self.ui.mpl_canvas.layout().addWidget(self._canvas)

    def _connect_signals(self):
        self.ui.spin_cycle.valueChanged.connect(self.ui.slider_cycle.setValue)
        self.ui.slider_cycle.valueChanged.connect(self.ui.spin_cycle.setValue)
        
        self.ui.spin_k_set.valueChanged.connect(lambda value: self._sync_slider_from_spin(self.ui.slider_k_set, self.ui.spin_k_set, value))
        self.ui.slider_k_set.valueChanged.connect(lambda value: self._sync_spin_from_slider(self.ui.slider_k_set, self.ui.spin_k_set, value))
        self.ui.spin_k_reset.valueChanged.connect(lambda value: self._sync_slider_from_spin(self.ui.slider_k_reset, self.ui.spin_k_reset, value))
        self.ui.slider_k_reset.valueChanged.connect(lambda value: self._sync_spin_from_slider(self.ui.slider_k_reset, self.ui.spin_k_reset, value))

        self.ui.spin_cycle.valueChanged.connect(self._on_cycle_changed)
        self.ui.slider_k_set.valueChanged.connect(self._on_params_changed)
        self.ui.slider_k_reset.valueChanged.connect(self._on_params_changed)

        self.ui.btn_apply.clicked.connect(self.apply_changes)
        self.ui.btn_cancel.clicked.connect(self.discard_changes)

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
        
        # update enabled
        for w in [self.ui.spin_cycle, self.ui.slider_cycle, self.ui.spin_k_set, self.ui.spin_k_reset, self.ui.slider_k_set, self.ui.slider_k_reset]:
            w.setEnabled(app_state_valid)

        # update initial values
        if (first_cycle_idx != first_cycle_idx_prev) or (last_cycle_idx != last_cycle_idx_prev):
            self.ui.spin_cycle.setValue(1)

        # update apply / cancel buttons
        ui_state = self._read_ui_state()
        has_changes = ui_state != self._state
        self.ui.btn_apply.setEnabled(has_changes)
        self.ui.btn_cancel.setEnabled(has_changes)

    def _on_cycle_changed(self):
        self.update_plot()

    def _on_params_changed(self):
        self._update_controls()
        self.update_plot()

    def apply_changes(self):
        ui_state = self._read_ui_state()
        self._state = ui_state

        self._app_state.k_set = self._state.k_set
        self._app_state.k_reset = self._state.k_reset

        self._app_state.R_on = np.array([])
        self._app_state.R_off = np.array([])
        self._app_state.V_set = np.array([])
        self._app_state.V_reset = np.array([])
        self._app_state.shottky_params = np.array([])
        
        self._update_controls()
        self.data_applied.emit()

    def discard_changes(self):
        self._sync_state_with_app_state()
        self._write_state_to_ui(self._state)
        self._update_controls()
        self.update_plot()
        self.data_discarded.emit()

    def update_plot(self):
        if not(self._app_state.is_source_data_valid()):
            self._line.set_data([], [])
            self._canvas.draw_idle()
            return

        i = self.ui.spin_cycle.value() - 1
        start, end = get_period_indices(self._app_state.V.size, i, self._app_state.V_zeros, segments_per_period=2, period_start_segment_idx=0)
        
        V = self._app_state.V[start : end]
        I = self._app_state.I[start : end]
        V_zeros = self._app_state.V_zeros[(self._app_state.V_zeros >= start) & (self._app_state.V_zeros <= end)] - start
        V0_idx = V_zeros[1]
        V_max_idx = self._app_state.V_maxima[i] - start
        V_min_idx = self._app_state.V_minima[i] - start

        self._line.set_data(V, I)

        period_samples = int(round(1 / self._app_state.V_freq / self._app_state.dt))
        I_smoothed = filter_current(I, period_samples, high_smooth=True, mode='wrap')
        on_index = get_on_index(V_max_idx, V_min_idx, starts_with_hrs=self._app_state.starts_with_hrs)
        off_index = get_off_index(V_max_idx, V_min_idx, starts_with_hrs=self._app_state.starts_with_hrs)
        set_index = detect_set(V, I_smoothed, on_index, V0_idx, k=self.ui.spin_k_set.value(), starts_with_hrs=self._app_state.starts_with_hrs)
        reset_index = detect_reset(V, I_smoothed, off_index, V0_idx, k=self.ui.spin_k_reset.value(), starts_with_hrs=self._app_state.starts_with_hrs)

        self._set_point.set_offsets([[V[set_index], I[set_index]]])
        self._reset_point.set_offsets([[V[reset_index], I[reset_index]]])

        self._ax.relim()
        self._ax.autoscale_view()
        self._canvas.draw_idle()

    def _sync_slider_from_spin(self, slider, spin, value: float):
        scale = slider.maximum() / spin.maximum()

        slider.blockSignals(True)
        slider.setValue(round(value * scale))
        slider.blockSignals(False)

    def _sync_spin_from_slider(self, slider, spin, value: int):
        scale = spin.maximum() / slider.maximum()

        spin.blockSignals(True)
        spin.setValue(value * scale)
        spin.blockSignals(False)

    def set_cycle(self, value: int):
        n_cycles = get_num_periods(self._app_state.V_zeros, segments_per_period=2)
        value = max(1, min(int(value), n_cycles))
        self.ui.spin_cycle.setValue(value)

    def get_cycle(self) -> int:
        return self.ui.spin_cycle.value()

    def is_modified(self) -> bool:
        return self._read_ui_state() != self._state