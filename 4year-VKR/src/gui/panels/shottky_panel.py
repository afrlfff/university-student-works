from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtCore import QFileInfo

from gui.ui_autogen.ui_shottky_panel import Ui_ShottkyPanel

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from gui.core.settings_storage import SettingsStorage
from gui.panels.base_panel import BasePanel
from core.algorithms import get_period_indices
from core.types import AppState
from core.plot import set_scientific_xaxis, set_scientific_yaxis
from core.memristor import extract_schottky_current, extract_memristive_current

class ShottkyPanel(BasePanel):
    def __init__(self, parent=None, app_state: AppState = None):
        super().__init__(parent, app_state)
        self.ui = Ui_ShottkyPanel()
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

        i = self.ui.spin_cycle.value() - 1 - self._app_state.first_cycle_idx
        phi, a_f, a_r, b_f, b_r = self._app_state.shottky_params[i]

        self.ui.le_phi.setText(str(phi))
        self.ui.le_alpha_f.setText(str(a_f))
        self.ui.le_alpha_r.setText(str(a_r))
        self.ui.le_beta_f.setText(str(b_f))
        self.ui.le_beta_r.setText(str(b_r))

        j = self.ui.spin_cycle.value() - 1
        start, end = get_period_indices(self._app_state.V.size, j, self._app_state.V_zeros, segments_per_period=2, period_start_segment_idx=0)
        
        V = self._app_state.V[start : end]
        I = self._app_state.I[start : end]
        I_s = extract_schottky_current(V, a_f, a_r, b_f, b_r)
        I_m = extract_memristive_current(I, phi, I_s)
    
        self._line_I.set_data(V, I)
        self._line_I_m.set_data(V, I_m)
            
        self._ax.relim()
        self._ax.autoscale_view()
        self._canvas.draw_idle()

    def _connect_signals(self):
        self.ui.slider_cycle.valueChanged.connect(self.ui.spin_cycle.setValue)
        self.ui.spin_cycle.valueChanged.connect(self.ui.slider_cycle.setValue)
        self.ui.spin_cycle.valueChanged.connect(self.update_plot)
        self.ui.chk_I.toggled.connect(self._on_I_toggle)
        self.ui.chk_Im.toggled.connect(self._on_Im_toggle)
        self.ui.btn_export.clicked.connect(self.export_data)

    def _update_controls(self):
        app_state_valid = self._app_state.is_source_data_valid()
        
        first_cycle_idx = (self._app_state.first_cycle_idx) if app_state_valid else 0
        last_cycle_idx = (self._app_state.last_cycle_idx) if app_state_valid else 0

        first_cycle_idx_prev = self.ui.spin_cycle.minimum() - 1
        last_cycle_idx_prev = self.ui.spin_cycle.maximum() - 1

        # update export btn
        valid = app_state_valid and self._app_state.shottky_params.size > 0
        self.ui.btn_export.setEnabled(valid)

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
        self._ax = self._canvas.figure.add_subplot()
        self._line_I, = self._ax.plot([], label="$I(t) = I_s(t) + I_m(t)$")
        self._line_I_m, = self._ax.plot([], label="$I_m(t)$")

        self.ui.mpl_canvas.layout().addWidget(self._canvas)

        self._ax.grid(True, alpha=0.3)
        self._ax.set_xlabel(self.tr("Напряжение, [В]"))
        self._ax.set_ylabel(self.tr("Ток, [А]"))
        set_scientific_xaxis(self._ax)
        set_scientific_yaxis(self._ax)
        self._ax.legend()

    def export_data(self):
        default_dir = SettingsStorage.get("export/shottky_params_dir", "")
        default_path = f"{default_dir}/shottky_params.txt" if default_dir else "shottky_params.txt"

        path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Экспорт параметров Шоттки"),
            default_path,
            self.tr("Text files (*.txt);;All files (*)"),
        )

        if not path:
            return

        export_dir = QFileInfo(path).absolutePath()
        SettingsStorage.set("export/shottky_params_dir", export_dir)
        SettingsStorage.sync()

        params = np.asarray(self._app_state.shottky_params)

        with open(path, "w", encoding="utf-8") as f:
            for row in params:
                f.write(" ".join(f"{value:g}" for value in row[:5]) + "\n")

    def _on_I_toggle(self, checked: bool):
        self._line_I.set_visible(checked)
        self._canvas.draw_idle()

    def _on_Im_toggle(self, checked: bool):
        self._line_I_m.set_visible(checked)
        self._canvas.draw_idle()

    def is_I_curve_enabled(self) -> bool:
        return self.ui.chk_I.isChecked()

    def is_Im_curve_enabled(self) -> bool:
        return self.ui.chk_Im.isChecked()

    def _set_phi(self, val: float): self.ui.le_phi.setText(f"{val:g}".replace(',', '.'))
    def _set_alpha_f(self, val: float): self.ui.le_alpha_f.setText(f"{val:g}".replace(',', '.'))
    def _set_alpha_r(self, val: float): self.ui.le_alpha_r.setText(f"{val:g}".replace(',', '.'))
    def _set_beta_f(self, val: float): self.ui.le_beta_f.setText(f"{val:g}".replace(',', '.'))
    def _set_beta_r(self, val: float): self.ui.le_beta_r.setText(f"{val:g}".replace(',', '.'))

    def get_phi(self) -> float:
        return float(self.ui.le_phi.text().replace(',', '.'))
    def get_alpha_f(self) -> float:
        return float(self.ui.le_alpha_f.text().replace(',', '.'))
    def get_alpha_r(self) -> float:
        return float(self.ui.le_alpha_r.text().replace(',', '.'))
    def get_beta_f(self) -> float:
        return float(self.ui.le_beta_f.text().replace(',', '.'))
    def get_beta_r(self) -> float:
        return float(self.ui.le_beta_r.text().replace(',', '.'))