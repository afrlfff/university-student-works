import numpy as np

from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QFileInfo
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from gui.ui_autogen.ui_ron_roff_panel import Ui_RonRoffPanel

from gui.core.settings_storage import SettingsStorage
from gui.panels.base_panel import BasePanel
from core.types import AppState
from core.plot import set_scientific_yaxis, set_scientific_xaxis


class RonRoffPanel(BasePanel):
    def __init__(self, parent=None, app_state: AppState = None):
        super().__init__(parent, app_state)
        self.ui = Ui_RonRoffPanel()
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
        valid = (self._app_state.is_source_data_valid()) and (self._app_state.shottky_params.size > 0)
        self.ui.btn_export.setEnabled(valid)

        self.ui.btn_trend.setEnabled(valid)
        self.ui.btn_distribution.setEnabled(valid)

    def _setup_plot(self):
        # canvas #1
        self._canvas_main = FigureCanvas(
            Figure(figsize=(5, 6), dpi=100, constrained_layout=True)
        )
        fig_main = self._canvas_main.figure
        self._ax_ron = fig_main.add_subplot(2, 1, 1)
        self._ax_roff = fig_main.add_subplot(2, 1, 2, sharex=self._ax_ron)

        self._line_ron, = self._ax_ron.plot([], [], label="$R_{ON}$")
        self._line_roff, = self._ax_roff.plot([], [], label="$R_{OFF}$")

        for ax in (self._ax_ron, self._ax_roff):
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_ylabel(self.tr("Сопротивление, [Ом]"))
            set_scientific_yaxis(ax)
            ax.legend()
        self._ax_roff.set_xlabel(self.tr("Номер цикла"))

        # canvas #2
        self._canvas_hist = FigureCanvas(
            Figure(figsize=(6, 3), dpi=100, constrained_layout=True)
        )
        fig_hist = self._canvas_hist.figure
        self._ax_hist_ron = fig_hist.add_subplot(1, 2, 1)
        self._ax_hist_roff = fig_hist.add_subplot(1, 2, 2)

        self._format_hist_axis(self._ax_hist_ron, "$R_{ON}$")
        self._format_hist_axis(self._ax_hist_roff, "$R_{OFF}$")

        self.ui.mpl_canvas_1.layout().addWidget(self._canvas_main)
        self.ui.mpl_canvas_2.layout().addWidget(self._canvas_hist)

    def update_plot(self):
        if not self._app_state.is_source_data_valid():
            self._clear_plot()
            return

        R_on = np.asarray(self._app_state.R_on)
        R_off = np.asarray(self._app_state.R_off)

        if R_on.size == 0 or R_off.size == 0:
            self._clear_plot()
            return

        cycles_on = np.arange(1, R_on.size + 1)
        cycles_off = np.arange(1, R_off.size + 1)

        # Ron / Roff по циклам
        self._line_ron.set_data(cycles_on, R_on)
        self._line_roff.set_data(cycles_off, R_off)

        for ax in (self._ax_ron, self._ax_roff):
            ax.relim()
            ax.autoscale_view()

        # Гистограммы
        self._update_histograms(R_on, R_off)

        self._canvas_main.draw_idle()
        self._canvas_hist.draw_idle()

    def _clear_plot(self):
        self._line_ron.set_data([], [])
        self._line_roff.set_data([], [])

        self._ax_hist_ron.cla()
        self._ax_hist_roff.cla()

        self._format_hist_axis(self._ax_hist_ron, "$R_{ON}$")
        self._format_hist_axis(self._ax_hist_roff, "$R_{OFF}$")

        self._canvas_main.draw_idle()
        self._canvas_hist.draw_idle()

    def _update_histograms(self, R_on, R_off):
        self._ax_hist_ron.cla()
        self._ax_hist_roff.cla()

        self._ax_hist_ron.hist(R_on, bins='auto')
        self._ax_hist_roff.hist(R_off, bins='auto')

        self._format_hist_axis(self._ax_hist_ron, "$R_{ON}$")
        self._format_hist_axis(self._ax_hist_roff, "$R_{OFF}$")

    def _format_hist_axis(self, ax, title: str):
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_title(title)
        ax.set_xlabel(self.tr("Сопротивление, [Ом]"))
        ax.set_ylabel(self.tr("Количество"))
        set_scientific_xaxis(ax)

    def export_data(self):
        default_dir = SettingsStorage.get("export/ron_roff_dir", "")
        default_path = f"{default_dir}/Ron_Roff.txt" if default_dir else "Ron_Roff.txt"

        path, _ = QFileDialog.getSaveFileName(
            self,
            self.tr("Экспорт Ron/Roff"),
            default_path,
            self.tr("Text files (*.txt);;All files (*)"),
        )

        if not path:
            return

        export_dir = QFileInfo(path).absolutePath()
        SettingsStorage.set("export/ron_roff_dir", export_dir)
        SettingsStorage.sync()

        R_on = np.asarray(self._app_state.R_on)
        R_off = np.asarray(self._app_state.R_off)

        n = min(R_on.size, R_off.size)

        with open(path, "w", encoding="utf-8") as f:
            for ron, roff in zip(R_on[:n], R_off[:n]):
                f.write(f"{ron} {roff}\n")