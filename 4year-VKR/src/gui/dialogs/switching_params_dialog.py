import numpy as np

from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtCore import QThread, Qt

from gui.ui_autogen.ui_ron_roff_dialog import Ui_RonRoffDialog
from gui.workers.switching_params_worker import SwitchingParamsWorker

from core.types import AppState


class SwitchingParamsDialog(QDialog):
    def __init__(self, app_state: AppState, parent=None):
        super().__init__(parent)
        self.ui = Ui_RonRoffDialog()
        self.ui.setupUi(self)

        self._threads = set()
        self._workers = set()
        self._closing = False

        self._app_state = app_state
        self._ron = np.array([])
        self._roff = np.array([])
        self._vset = np.array([])
        self._vreset = np.array([])

        self._num_cycles = app_state.last_cycle_idx - app_state.first_cycle_idx + 1

        self.ui.prog.setMinimum(0)
        self.ui.prog.setMaximum(self._num_cycles)
        self.ui.prog.setValue(0)

        self.ui.btn_interrupt.clicked.connect(self._on_cancel)

        self._init_process()

    def _init_process(self):
        worker = SwitchingParamsWorker(self._app_state)
        thread = QThread()
        worker.moveToThread(thread)

        thread.started.connect(worker.run_task, Qt.QueuedConnection)

        worker.iteration_finished.connect(self._on_iteration_finished, Qt.QueuedConnection)
        worker.data_ready.connect(self._on_data_ready, Qt.QueuedConnection)
        worker.error_occurred.connect(self._on_error, Qt.QueuedConnection)

        worker.finished.connect(thread.quit)
        worker.finished.connect(lambda w=worker: self._on_worker_finished(w))
        thread.finished.connect(lambda t=thread: self._on_thread_finished(t))

        self._threads.add(thread)
        self._workers.add(worker)

        thread.start()

    def _on_thread_finished(self, thread):
        self._threads.discard(thread)
        thread.deleteLater()

    def _on_worker_finished(self, worker):
        self._workers.discard(worker)
        worker.deleteLater()

    def _on_iteration_finished(self, i: int):
        self.ui.prog.setValue(i)

    def _on_data_ready(self, ron, roff, vset, vreset):
        self._ron = ron
        self._roff = roff
        self._vset = vset
        self._vreset = vreset

        self._ensure_stop()
        self.accept()

    def _on_error(self, error_msg: str):
        self.ui.lbl.setText(
            self.tr("Возникла ошибка. Расчет прерван.\nТекст ошибки: ")
            + error_msg
        )
        self.ui.btn_interrupt.setText(self.tr("Ок"))
        self._request_shutdown()

    def get_ron(self):
        return self._ron

    def get_roff(self):
        return self._roff
    
    def get_vset(self):
        return self._vset

    def get_vreset(self):
        return self._vreset

    def _request_shutdown(self):
        for thread in list(self._threads):
            thread.requestInterruption()
            thread.quit()

    def _ensure_stop(self):
        if self._threads:
            self._request_shutdown()

            for thread in list(self._threads):
                thread.wait(1000)

                if thread.isRunning():
                    thread.terminate()
                    thread.wait()

            self._threads.clear()
            self._workers.clear()

    def closeEvent(self, event):
        self._close()
        event.accept()

    def _on_cancel(self):
        self._close()

    def _close(self):
        if self._closing:
            return

        self._closing = True

        self.ui.lbl.setText(self.tr("Закрытие окна ..."))
        QApplication.processEvents()

        self._ensure_stop()
        self.reject()