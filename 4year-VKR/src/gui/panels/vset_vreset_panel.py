import numpy as np

from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QFileInfo
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from gui.ui_autogen.ui_vset_vreset_panel import Ui_VsetVresetPanel

from gui.core.settings_storage import SettingsStorage
from gui.panels.base_panel import BasePanel
from core.types import AppState
from core.plot import set_scientific_yaxis, set_scientific_xaxis


class VsetVresetPanel(BasePanel):
    def __init__(self, parent=None, app_state: AppState = None):
        super().__init__(parent, app_state)
        self.ui = Ui_VsetVresetPanel()
        self.ui.setupUi(self)

        self._setup_plot()
        self._connect_signals()
        self.sync()

    def sync(self):
        self._update_controls()
        self.update_plot()
        self._show_trend_plot()

    def _connect_signals(self):
        self.ui.btn_export.clicked.connect(self.export_data)
        self.ui.btn_trend.clicked.connect(self._show_trend_plot)
        self.ui.btn_distribution.clicked.connect(self._show_distribution_plot)

    def _show_trend_plot(self):
        self.ui.stack.setCurrentWidget(self.ui.mpl_canvas_1)

        self.ui.btn_trend.setEnabled(False)
        self.ui.btn_distribution.setEnabled(True)

    def _show_distribution_plot(self):
        self.ui.stack.setCurrentWidget(self.ui.mpl_canvas_2)

        self.ui.btn_trend.setEnabled(True)
        self.ui.btn_distribution.setEnabled(False)

    def _update_controls(self):
        valid = (
            self._app_state.is_source_data_valid()
            and self._app_state.shottky_params.size > 0
        )

        self.ui.btn_export.setEnabled(valid)
        self.ui.btn_trend.setEnabled(valid)
        self.ui.btn_distribution.setEnabled(valid)

    def _setup_plot(self):
        # canvas #1
        self._canvas_main = FigureCanvas(
            Figure(figsize=(5, 6), dpi=100, constrained_layout=True)
        )
        fig_main = self._canvas_main.figure
        self._ax_vset = fig_main.add_subplot(2, 1, 1)
        self._ax_vreset = fig_main.add_subplot(2, 1, 2, sharex=self._ax_vset)

        self._line_vset, = self._ax_vset.plot([], [], label="$V_{SET}$")
        self._line_vreset, = self._ax_vreset.plot([], [], label="$V_{RESET}$")

        for ax in (self._ax_vset, self._ax_vreset):
            ax.grid(True, alpha=0.3, linestyle="--")
            ax.set_ylabel(self.tr("Напряжение, [В]"))
            set_scientific_yaxis(ax)
            ax.legend()

        self._ax_vreset.set_xlabel(self.tr("Номер цикла"))

        # canvas #2
        self._canvas_hist = FigureCanvas(
            Figure(figsize=(6, 3), dpi=100, constrained_layout=True)
        )
        fig_hist = self._canvas_hist.figure
        self._ax_hist_vset = fig_hist.add_subplot(1, 2, 1)
        self._ax_hist_vreset = fig_hist.add_subplot(1, 2, 2)

        self._format_hist_axis(self._ax_hist_vset, "$V_{SET}$")
        self._format_hist_axis(self._ax_hist_vreset, "$V_{RESET}$")

        self.ui.mpl_canvas_1.layout().addWidget(self._canvas_main)
        self.ui.mpl_canvas_2.layout().addWidget(self._canvas_hist)

    def update_plot(self):
        if not self._app_state.is_source_data_valid():
            self._clear_plot()
            return

        V_set = np.asarray(self._app_state.V_set)
        V_reset = np.asarray(self._app_state.V_reset)

        if V_set.size == 0 or V_reset.size == 0:
            self._clear_plot()
            return

        cycles_set = np.arange(1, V_set.size + 1)
        cycles_reset = np.arange(1, V_reset.size + 1)

        # Vset / Vreset по циклам
        self._line_vset.set_data(cycles_set, V_set)
        self._line_vreset.set_data(cycles_reset, V_reset)

        for ax in (self._ax_vset, self._ax_vreset):
            ax.relim()
            ax.autoscale_view()

        # Гистограммы
        self._update_histograms(V_set, V_reset)

        self._canvas_main.draw_idle()
        self._canvas_hist.draw_idle()

    def _clear_plot(self):
        self._line_vset.set_data([], [])
        self._line_vreset.set_data([], [])

        self._ax_hist_vset.cla()
        self._ax_hist_vreset.cla()

        self._format_hist_axis(self._ax_hist_vset, "$V_{SET}$")
        self._format_hist_axis(self._ax_hist_vreset, "$V_{RESET}$")

        self._canvas_main.draw_idle()
        self._canvas_hist.draw_idle()

    def _update_histograms(self, V_set, V_reset):
        self._ax_hist_vset.cla()
        self._ax_hist_vreset.cla()

        self._ax_hist_vset.hist(V_set, bins='auto')
        self._ax_hist_vreset.hist(V_reset, bins='auto')

        self._format_hist_axis(self._ax_hist_vset, "$V_{SET}$")
        self._format_hist_axis(self._ax_hist_vreset, "$V_{RESET}$")

    def _format_hist_axis(self, ax, title: str):
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.set_title(title)
        ax.set_xlabel(self.tr("Напряжение, [В]"))
        ax.set_ylabel(self.tr("Количество"))
        set_scientific_xaxis(ax, scilimits=(-2, 2))

    def export_data(self):
        default_dir = SettingsStorage.get("export/vset_vreset_dir", "")
        default_path = f"{default_dir}/Vset_Vreset.txt" if default_dir else "Vset_Vreset.txt"

        path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Экспорт Vset/Vreset"),
            default_path,
            self.tr("Text files (*.txt);;All files (*)"),
        )

        if not path:
            return

        export_dir = QFileInfo(path).absolutePath()
        SettingsStorage.set("export/vset_vreset_dir", export_dir)
        SettingsStorage.sync()

        V_set = np.asarray(self._app_state.V_set)
        V_reset = np.asarray(self._app_state.V_reset)

        n = min(V_set.size, V_reset.size)

        with open(path, "w", encoding="utf-8") as f:
            for vset, vreset in zip(V_set[:n], V_reset[:n]):
                f.write(f"{vset} {vreset}\n")
