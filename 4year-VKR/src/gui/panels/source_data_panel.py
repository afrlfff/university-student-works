import os
from dataclasses import dataclass
from PySide6.QtWidgets import QWidget, QFileDialog, QDialog
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression, Signal
from gui.ui_autogen.ui_source_data_panel import Ui_SourceDataPanel

from gui.panels.base_panel import BasePanel
from gui.dialogs.data_read_dialog import DataReadDialog
from gui.core.settings_storage import SettingsStorage
from core.types import AppState
from core.algorithms import get_num_periods

@dataclass
class SourceDataState:
    vin_path: str = ""
    vout_path: str = ""
    dt: float = 0.0
    r: int = 1
    r_nominal_idx: int = 1

    def get_r(self) -> float:
        multipliers = [0.001, 1, 1000]
        return self.r * multipliers[self.r_nominal_idx]
    
    def is_valid(self) -> bool:
        return (
            os.path.isfile(self.vin_path)
            and os.path.isfile(self.vout_path)
            and self.dt > 0
            and self.r > 0
            and self.r_nominal_idx >= 0 and self.r_nominal_idx <= 2
        )

class SourceDataPanel(BasePanel):
    read_started = Signal()
    read_failed = Signal()
    read_finished = Signal()

    data_applied = Signal()
    data_discarded = Signal()

    def __init__(self, parent=None, app_state: AppState = None):
        super().__init__(parent, app_state)
        self.ui = Ui_SourceDataPanel()
        self.ui.setupUi(self)

        self._storage_prefix = "source_data_panel"
        self._state = SourceDataState()

        self._setup_ui()
        self._connect_signals()
        self.load_settings()
        
        self.ui.btn_apply.setEnabled(True)

    def sync(self):
        pass

    def save_settings(self):
        SettingsStorage.set(f"{self._storage_prefix}/V_in_path", self._state.vin_path)
        SettingsStorage.set(f"{self._storage_prefix}/V_out_path", self._state.vout_path)
        SettingsStorage.set(f"{self._storage_prefix}/R", self._state.r)
        SettingsStorage.set(f"{self._storage_prefix}/R_nominal_idx", self._state.r_nominal_idx)
        SettingsStorage.set(f"{self._storage_prefix}/dt", self._state.dt)
        SettingsStorage.sync()

    def load_settings(self):
        self._state = SourceDataState(
            vin_path=SettingsStorage.get(f"{self._storage_prefix}/V_in_path", ""),
            vout_path=SettingsStorage.get(f"{self._storage_prefix}/V_out_path", ""),
            r=SettingsStorage.get(f"{self._storage_prefix}/R", 1),
            r_nominal_idx=SettingsStorage.get(f"{self._storage_prefix}/R_nominal_idx", 1),
            dt=float(SettingsStorage.get(f"{self._storage_prefix}/dt", 0)),
        )

        self._write_state_to_ui(self._state)
        self._update_controls()

    def apply_changes(self):
        ui_state = self._read_ui_state()
        if not ui_state.is_valid():
            return
        
        self._app_state.clear()
        data_read_dialog = DataReadDialog(ui_state.vin_path, ui_state.vout_path, ui_state.get_r(), ui_state.dt, parent=self)
        self.read_started.emit()

        if data_read_dialog.exec() == QDialog.DialogCode.Accepted:
            self._app_state.dt = ui_state.dt
            self._app_state.R = ui_state.get_r()
            self._app_state.V = data_read_dialog.get_V()
            self._app_state.I = data_read_dialog.get_I()
            self._app_state.V_zeros = data_read_dialog.get_Vzeros()
            self._app_state.V_maxima = data_read_dialog.get_Vmaxima()
            self._app_state.V_minima = data_read_dialog.get_Vminima()
            self._app_state.V_freq = data_read_dialog.get_V_freq()
            self._app_state.first_cycle_idx = 0
            self._app_state.last_cycle_idx = get_num_periods(self._app_state.V_zeros, segments_per_period=2) - 1
            self._app_state.k_set = 1.0
            self._app_state.k_reset = 1.0

            period_samples = round(1 / self._app_state.V_freq / self._app_state.dt )
            self._app_state.g_break_length = int(round(0.1 * period_samples))
            self._app_state.g_break_length += int(self._app_state.g_break_length % 2 == 0)

            self._state = ui_state
            self.save_settings()
            self._update_controls()
            self.read_finished.emit()
        else:
            self.read_failed.emit()

    def discard_changes(self):
        self._write_state_to_ui(self._state)
        self._update_controls()
        self.data_discarded.emit()

    def _read_ui_state(self) -> SourceDataState:
        dt_text = self.ui.le_dt.text().strip() if self.ui.le_dt.hasAcceptableInput() else ""
        dt = float(dt_text) if (dt_text) else 0.0

        return SourceDataState(
            vin_path=self.ui.le_Vin.text().strip(),
            vout_path=self.ui.le_Vout.text().strip(),
            dt=dt,
            r=self.ui.spin_R.value(),
            r_nominal_idx=self.ui.cmb_R_nominal.currentIndex(),
        )

    def _write_state_to_ui(self, state: SourceDataState):
        self.ui.le_Vin.setText(state.vin_path)
        self.ui.le_Vout.setText(state.vout_path)

        self.ui.spin_R.setValue(state.r)
        self.ui.cmb_R_nominal.setCurrentIndex(state.r_nominal_idx)

        if state.dt > 0:
            self.ui.le_dt.setText(f"{state.dt:.9f}".rstrip("0").rstrip("."))
        else:
            self.ui.le_dt.clear()

    def _setup_ui(self):
        units = ["мОм", "Ом", "кОм"]
        self.ui.cmb_R_nominal.clear()
        for unit in units:
            self.ui.cmb_R_nominal.addItem(self.tr(unit))
        self.ui.cmb_R_nominal.setCurrentIndex(1)

        # Опциональная целая часть + обязательная точка + обязательная дробная часть
        regex = QRegularExpression(r"^\d*\.\d+$")
        self.ui.le_dt.setValidator(QRegularExpressionValidator(regex))

    def _connect_signals(self):
        self.ui.btn_select_Vin.clicked.connect(lambda: self._select_file(self.ui.le_Vin, root_dir=self._get_root_dir(self.ui.le_Vin)))
        self.ui.btn_select_Vout.clicked.connect(lambda: self._select_file(self.ui.le_Vout, root_dir=self._get_root_dir(self.ui.le_Vout)))

        self.ui.btn_apply.clicked.connect(self.apply_changes)
        self.ui.btn_cancel.clicked.connect(self.discard_changes)

        self.ui.le_Vin.textChanged.connect(self._update_controls)
        self.ui.le_Vout.textChanged.connect(self._update_controls)
        self.ui.le_dt.textChanged.connect(self._update_controls)
        self.ui.spin_R.valueChanged.connect(self._update_controls)
        self.ui.cmb_R_nominal.currentIndexChanged.connect(self._update_controls)

    def _update_controls(self):
        ui_state = self._read_ui_state()
        has_changes = ui_state != self._state

        self.ui.btn_apply.setEnabled((has_changes and ui_state.is_valid()) or not(self._app_state.is_source_data_valid()))
        self.ui.btn_cancel.setEnabled(has_changes)

    def _get_root_dir(self, line_edit):
        return os.path.dirname(line_edit.text()) if (line_edit.text()) else (None)

    def _select_file(self, target_line_edit, root_dir=None):
        if root_dir is None:
            path, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        else:
            path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", root_dir)
        
        if path:
            target_line_edit.setText(path)

    def is_valid_data(self) -> bool:
        return self._state.is_valid()

    def get_Vin_path(self) -> str:
        return self._state.vin_path

    def get_Vout_path(self) -> str:
        return self._state.vout_path

    def get_dt(self) -> float:
        return self._state.dt

    def get_r(self) -> float:
        return self._state.get_r()
    
    def get_app_state(self):
        return self._app_state
    
