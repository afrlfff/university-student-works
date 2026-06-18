from PySide6.QtWidgets import QMainWindow, QWidget

from gui.ui_autogen.ui_main_window import Ui_MainWindow

from gui.panels.source_data_panel import SourceDataPanel
from gui.panels.num_cycles_panel import NumCyclesPanel
from gui.panels.set_reset_panel import SetResetPanel
from gui.panels.shottky_panel import ShottkyPanel
from gui.panels.shottky_search_panel import ShottkySearchPanel
from gui.panels.switching_params_calc_panel import SwitchingParamsCalcPanel
from gui.panels.state_X_panel import StateXPanel
from gui.panels.ron_roff_panel import RonRoffPanel
from gui.panels.vset_vreset_panel import VsetVresetPanel

from gui.panels.base_panel import BasePanel
from core.types import AppState

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._app_state = AppState()

        self._setup_styles()
        self._setup_pages()
        self._connect_signals()
        self._update_controls()

        self.ui.stack.setCurrentWidget(self._source_data_panel)
        self._set_current_button(self.ui.btn_data_load)

    def _setup_styles(self):
        self.setStyleSheet("""
        QPushButton[current="true"] {
            background-color:  rgb(60, 75, 105);
        }
        """)

    def _set_current_button(self, current_btn):
        for btn in self._page_buttons.values():
            btn.setProperty("current", btn is current_btn)

            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    def _setup_pages(self):
        self._source_data_panel = SourceDataPanel(parent=self.ui.stack, app_state=self._app_state)
        self._num_cycles_panel = NumCyclesPanel(parent=self.ui.stack, app_state=self._app_state)
        self._set_reset_panel = SetResetPanel(parent=self.ui.stack, app_state=self._app_state)
        self._shottky_panel = ShottkyPanel(parent=self.ui.stack, app_state=self._app_state)
        self._shottky_search_panel = ShottkySearchPanel(parent=self.ui.stack, app_state=self._app_state)
        self._switching_params_calc_panel = SwitchingParamsCalcPanel(parent=self.ui.stack, app_state=self._app_state)
        self._state_X_panel = StateXPanel(parent=self.ui.stack, app_state=self._app_state)
        self._ron_roff_panel = RonRoffPanel(parent=self.ui.stack, app_state=self._app_state)
        self._vset_vreset_panel = VsetVresetPanel(parent=self.ui.stack, app_state=self._app_state)

        self._add_page(self._source_data_panel)
        self._add_page(self._num_cycles_panel)
        self._add_page(self._set_reset_panel)
        self._add_page(self._shottky_panel)
        self._add_page(self._shottky_search_panel)
        self._add_page(self._switching_params_calc_panel)
        self._add_page(self._state_X_panel)
        self._add_page(self._ron_roff_panel)
        self._add_page(self._vset_vreset_panel)

        self._page_buttons = {
            self._source_data_panel: self.ui.btn_data_load,
            self._num_cycles_panel: self.ui.btn_num_cycles,
            self._set_reset_panel: self.ui.btn_set_reset,
            self._shottky_search_panel: self.ui.btn_shottky_search,
            self._switching_params_calc_panel: self.ui.btn_switching_params_calc,
            self._shottky_panel: self.ui.btn_shottky,
            self._state_X_panel: self.ui.btn_state_X,
            self._ron_roff_panel: self.ui.btn_ron_roff,
            self._vset_vreset_panel: self.ui.btn_vset_vreset,
        }

    def _connect_signals(self):
        self.ui.btn_data_load.clicked.connect(lambda: self._set_page(self._source_data_panel))
        self.ui.btn_num_cycles.clicked.connect(lambda: self._set_page(self._num_cycles_panel))
        self.ui.btn_set_reset.clicked.connect(lambda: self._set_page(self._set_reset_panel))
        self.ui.btn_shottky_search.clicked.connect(lambda: self._set_page(self._shottky_search_panel))
        self.ui.btn_switching_params_calc.clicked.connect(lambda: self._set_page(self._switching_params_calc_panel))
        self.ui.btn_shottky.clicked.connect(lambda: self._set_page(self._shottky_panel))
        self.ui.btn_state_X.clicked.connect(lambda: self._set_page(self._state_X_panel))
        self.ui.btn_ron_roff.clicked.connect(lambda: self._set_page(self._ron_roff_panel))
        self.ui.btn_vset_vreset.clicked.connect(lambda: self._set_page(self._vset_vreset_panel))

        self._source_data_panel.read_finished.connect(self._update_controls)
        self._source_data_panel.read_failed.connect(self._update_controls)
        self._num_cycles_panel.data_applied.connect(self._update_controls)
        self._num_cycles_panel.data_discarded.connect(self._update_controls)
        self._shottky_search_panel.search_finished.connect(self._update_controls)
        self._shottky_search_panel.search_failed.connect(self._update_controls)
        self._switching_params_calc_panel.calc_finished.connect(self._update_controls)
        self._switching_params_calc_panel.calc_failed.connect(self._update_controls)

    def _add_page(self, widget: QWidget):
        widget.setObjectName(f"page_{widget.__class__.__name__}")
        self.ui.stack.addWidget(widget)

    def _set_page(self, widget: QWidget):
        if isinstance(widget, BasePanel):
            widget.sync()

        self._update_controls()
        self.ui.stack.setCurrentWidget(widget)
        btn = self._page_buttons.get(widget)
        if btn is not None:
            self._set_current_button(btn)

    def _update_controls(self):
        has_source_data = self._app_state.is_source_data_valid()
        has_shottky_params = self._app_state.shottky_params.size > 0
        has_switching_params = (
            self._app_state.R_on.size > 0
            and self._app_state.R_off.size > 0
            and self._app_state.V_set.size > 0
            and self._app_state.V_reset.size > 0
        )

        self.ui.btn_data_load.setEnabled(True)

        self.ui.btn_num_cycles.setEnabled(has_source_data)
        self.ui.btn_set_reset.setEnabled(has_source_data)
        self.ui.btn_shottky_search.setEnabled(has_source_data)
        self.ui.btn_switching_params_calc.setEnabled(has_source_data and has_shottky_params)

        self.ui.btn_shottky.setEnabled(has_source_data and has_shottky_params)
        self.ui.btn_state_X.setEnabled(has_source_data and has_shottky_params)
        self.ui.btn_ron_roff.setEnabled(has_source_data and has_switching_params)
        self.ui.btn_vset_vreset.setEnabled(has_source_data and has_switching_params)