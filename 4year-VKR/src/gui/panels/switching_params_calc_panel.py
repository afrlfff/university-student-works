from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Signal
from gui.ui_autogen.ui_SwitchingParamsCalcPanel import Ui_SwitchingParamsCalcPanel

import numpy as np
from gui.panels.base_panel import BasePanel
from core.types import AppState
from gui.dialogs.switching_params_dialog import SwitchingParamsDialog

class SwitchingParamsCalcPanel(BasePanel):
    calc_started = Signal()
    calc_finished = Signal()
    calc_failed = Signal()

    def __init__(self, parent=None, app_state: AppState = None):
        super().__init__(parent, app_state)
        self.ui = Ui_SwitchingParamsCalcPanel()
        self.ui.setupUi(self)

        self.ui.btn_run.clicked.connect(self._on_run)
        
        self.sync()

    def sync(self):
        switching_params_set = \
            (self._app_state.R_on.size > 0) and \
            (self._app_state.R_off.size > 0) and \
            (self._app_state.V_set.size > 0) and \
            (self._app_state.V_reset.size > 0)
        self.ui.btn_run.setEnabled((self._app_state.shottky_params.size > 0) and not(switching_params_set))

    def _on_run(self):
        self._app_state.R_on = np.array([])
        self._app_state.R_off = np.array([])
        self._app_state.V_set = np.array([])
        self._app_state.V_reset = np.array([])
        switching_params_dialog = SwitchingParamsDialog(self._app_state, parent=self)
        self.calc_started.emit()

        if switching_params_dialog.exec() == QDialog.DialogCode.Accepted:
            self._app_state.R_on = switching_params_dialog.get_ron()
            self._app_state.R_off = switching_params_dialog.get_roff()
            self._app_state.V_set = switching_params_dialog.get_vset()
            self._app_state.V_reset = switching_params_dialog.get_vreset()

            self.ui.btn_run.setEnabled(False)
            self.calc_finished.emit()
        else:
            self.calc_failed.emit()