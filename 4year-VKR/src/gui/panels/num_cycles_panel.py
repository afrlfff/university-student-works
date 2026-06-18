from dataclasses import dataclass
import numpy as np

from PySide6.QtCore import QSignalBlocker, Signal

from gui.ui_autogen.ui_num_cycles_panel import Ui_NumCyclesPanel
from gui.panels.base_panel import BasePanel

from core.types import AppState
from core.algorithms import get_num_periods, get_period_indices


@dataclass
class NumCyclesState:
    first_cycle_idx: int = 0
    last_cycle_idx: int = 0


class NumCyclesPanel(BasePanel):
    data_applied = Signal()
    data_discarded = Signal()

    def __init__(self, parent=None, app_state: AppState = None):
        super().__init__(parent, app_state)
        self.ui = Ui_NumCyclesPanel()
        self.ui.setupUi(self)

        self._state = NumCyclesState()

        self._setup_ui()
        self._connect_signals()

        self._write_state_to_ui(self._state)
        self._update_controls()
        self.sync()

    def sync(self):
        if self._has_changes():
            self._update_controls()
            return

        self._sync_state_with_app_state()
        self._update_ranges_for_state(self._state)
        self._write_state_to_ui(self._state)
        self._update_controls()

    def _has_changes(self) -> bool:
        return self._app_state.is_source_data_valid() and self._read_ui_state() != self._state
    
    def _setup_ui(self):
        for w in (
            self.ui.spin_first_cycle,
            self.ui.slider_first_cycle,
            self.ui.spin_num_cycles,
            self.ui.slider_num_cycles,
        ):
            w.setMinimum(1)
            w.setMaximum(1)

        self.ui.le_tstart.setReadOnly(True)
        self.ui.le_tend.setReadOnly(True)

    def _connect_signals(self):
        self.ui.slider_first_cycle.valueChanged.connect(self.ui.spin_first_cycle.setValue)
        self.ui.spin_first_cycle.valueChanged.connect(self.ui.slider_first_cycle.setValue)

        self.ui.slider_num_cycles.valueChanged.connect(self.ui.spin_num_cycles.setValue)
        self.ui.spin_num_cycles.valueChanged.connect(self.ui.slider_num_cycles.setValue)

        self.ui.spin_first_cycle.valueChanged.connect(self._on_first_cycle_changed)
        self.ui.slider_first_cycle.valueChanged.connect(self._on_first_cycle_changed)

        self.ui.spin_num_cycles.valueChanged.connect(self._update_controls)
        self.ui.slider_num_cycles.valueChanged.connect(self._update_controls)

        self.ui.btn_apply.clicked.connect(self.apply_changes)
        self.ui.btn_cancel.clicked.connect(self.discard_changes)

    def _sync_state_with_app_state(self):
        if not self._app_state.is_source_data_valid():
            self._state = NumCyclesState()
            return

        self._state = NumCyclesState(
            first_cycle_idx=self._app_state.first_cycle_idx,
            last_cycle_idx=self._app_state.last_cycle_idx,
        )

    def _get_total_num_cycles(self) -> int:
        if not self._app_state.is_source_data_valid():
            return 1

        return max(
            1,
            get_num_periods(self._app_state.V_zeros, segments_per_period=2),
        )

    def _read_ui_state(self) -> NumCyclesState:
        first_cycle_idx = self.ui.spin_first_cycle.value() - 1
        num_cycles = self.ui.spin_num_cycles.value()
        last_cycle_idx = first_cycle_idx + num_cycles - 1

        return NumCyclesState(
            first_cycle_idx=first_cycle_idx,
            last_cycle_idx=last_cycle_idx,
        )

    def _write_state_to_ui(self, state: NumCyclesState):
        first_cycle = state.first_cycle_idx + 1
        num_cycles = state.last_cycle_idx - state.first_cycle_idx + 1
        num_cycles = max(1, num_cycles)

        with (
            QSignalBlocker(self.ui.spin_first_cycle),
            QSignalBlocker(self.ui.slider_first_cycle),
            QSignalBlocker(self.ui.spin_num_cycles),
            QSignalBlocker(self.ui.slider_num_cycles),
        ):
            self.ui.spin_first_cycle.setValue(first_cycle)
            self.ui.slider_first_cycle.setValue(first_cycle)

            self.ui.spin_num_cycles.setValue(num_cycles)
            self.ui.slider_num_cycles.setValue(num_cycles)

        self._update_time_fields()

    def _on_first_cycle_changed(self):
        self._update_ranges_for_state(self._read_ui_state())
        self._update_time_fields()
        self._update_controls()

    def _update_ranges_for_state(self, state: NumCyclesState):
        total_num_cycles = self._get_total_num_cycles()

        first_cycle = state.first_cycle_idx + 1
        first_cycle = max(1, min(first_cycle, total_num_cycles))

        max_num_cycles = total_num_cycles - first_cycle + 1
        max_num_cycles = max(1, max_num_cycles)

        with (
            QSignalBlocker(self.ui.spin_first_cycle),
            QSignalBlocker(self.ui.slider_first_cycle),
            QSignalBlocker(self.ui.spin_num_cycles),
            QSignalBlocker(self.ui.slider_num_cycles),
        ):
            self.ui.spin_first_cycle.setMinimum(1)
            self.ui.slider_first_cycle.setMinimum(1)
            self.ui.spin_first_cycle.setMaximum(total_num_cycles)
            self.ui.slider_first_cycle.setMaximum(total_num_cycles)

            self.ui.spin_num_cycles.setMinimum(1)
            self.ui.slider_num_cycles.setMinimum(1)
            self.ui.spin_num_cycles.setMaximum(max_num_cycles)
            self.ui.slider_num_cycles.setMaximum(max_num_cycles)

        self.ui.lbl_first_cycle_min.setText("1")
        self.ui.lbl_first_cycle_max.setText(str(total_num_cycles))
        self.ui.lbl_num_cycles_max.setText(str(max_num_cycles))

    def _update_controls(self):
        valid = self._app_state.is_source_data_valid()
        total_num_cycles = self._get_total_num_cycles()

        first_cycle_max = total_num_cycles

        for w in (self.ui.spin_first_cycle, self.ui.slider_first_cycle):
            w.setMinimum(1)
            w.setMaximum(first_cycle_max)

        self.ui.lbl_first_cycle_min.setText("1")
        self.ui.lbl_first_cycle_max.setText(str(first_cycle_max))

        self._update_ranges_for_state(self._read_ui_state())

        self.ui.wgt_cycles.setEnabled(valid)

        ui_state = self._read_ui_state()
        has_changes = valid and (ui_state != self._state)

        self.ui.btn_apply.setEnabled(has_changes)
        self.ui.btn_cancel.setEnabled(has_changes)

        self._update_time_fields()

    def _update_time_fields(self):
        i = self.ui.spin_first_cycle.value() - 1
        start, _ = get_period_indices(self._app_state.V.size, i, self._app_state.V_zeros, segments_per_period=2, period_start_segment_idx=0)
        t_start = start * self._app_state.dt
        self.ui.le_tstart.setText(f"{t_start:g}")

        i = self.ui.spin_first_cycle.value() + self.ui.spin_num_cycles.value() - 2
        _, end = get_period_indices(self._app_state.V.size, i, self._app_state.V_zeros, segments_per_period=2, period_start_segment_idx=0)
        t_end = end * self._app_state.dt
        self.ui.le_tend.setText(f"{t_end:g}")

    def apply_changes(self):
        self._state = self._read_ui_state()

        self._app_state.first_cycle_idx = self._state.first_cycle_idx
        self._app_state.last_cycle_idx = self._state.last_cycle_idx

        self._app_state.R_on = np.array([])
        self._app_state.R_off = np.array([])
        self._app_state.V_set = np.array([])
        self._app_state.V_reset = np.array([])
        self._app_state.shottky_params = np.array([])

        self._update_controls()
        self.data_applied.emit()

    def discard_changes(self):
        self._write_state_to_ui(self._state)
        self._update_controls()
        self.data_discarded.emit()