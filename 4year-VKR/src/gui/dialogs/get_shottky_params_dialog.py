import numpy as np
from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtCore import QThread, Qt
from gui.ui_autogen.ui_get_shottky_params_dialog import Ui_GetShottkyParamsDialog

from gui.workers.get_shottky_params_worker import GetShottkyParamsWorker

from core.types import AppState

class GetShottkyParamsDialog(QDialog):
    def __init__(self, app_state: AppState, parent=None):
        super().__init__(parent)
        self.ui = Ui_GetShottkyParamsDialog()
        self.ui.setupUi(self)

        self._threads = set()
        self._workers = set()
        self._app_state = app_state
        self._shottky_params = np.array([])

        self._num_cycles = app_state.last_cycle_idx - app_state.first_cycle_idx + 1

        self.ui.prog.setMinimum(0)
        self.ui.prog.setMaximum(self._num_cycles)
        self.ui.prog.setValue(0)
        
        self.ui.btn_interrupt.clicked.connect(self._on_cancel)

        self._init_process()

    def _init_process(self):
        worker = GetShottkyParamsWorker(self._app_state)
        thread = QThread()
        worker.moveToThread(thread)

        # Гарантируем выполнение в worker-потоке, а не в GUI
        thread.started.connect(worker.run_task, Qt.QueuedConnection)
        worker.params_found.connect(self._on_params_found, Qt.QueuedConnection)
        worker.error_occurred.connect(self._on_error, Qt.QueuedConnection)
        
        # Безопасная цепочка завершения
        worker.finished.connect(thread.quit)
        worker.finished.connect(lambda w=worker: self._on_worker_finished(w))
        thread.finished.connect(lambda t=thread: self._on_thread_finished(t))

        # доп. сигнал
        worker.param_found.connect(self._on_param_found)

        self._threads.add(thread)
        self._workers.add(worker)
        
        thread.start()

    def _on_thread_finished(self, thread):
        self._threads.discard(thread)
        thread.deleteLater()

    def _on_worker_finished(self, worker):
        self._workers.discard(worker)
        worker.deleteLater()

    def _on_param_found(self, i):
        self.ui.prog.setValue(i)

    def _on_params_found(self, params):
        self._shottky_params = params

        self._ensure_stop()
        self.accept()

    def get_params(self):
        return self._shottky_params

    def _on_error(self, erorr_msg: str):
        self.ui.lbl.setText(f"Возникла ошибка. Поиск прерван.\nТекст ошибки: {erorr_msg}")
        self.ui.btn_interrupt.setText(self.tr("Ок"))
        self._request_shutdown()

    def _request_shutdown(self):
        for thread in list(self._threads):
            thread.requestInterruption()
            thread.quit()

    def _ensure_stop(self):
        if self._threads:
            self._request_shutdown()
            
            for thread in list(self._threads):
                thread.wait(1000)
                
                # аварийное завершение
                if thread.isRunning():
                    thread.terminate()
                    thread.wait()

            self._threads.clear()
            self._workers.clear()

    def closeEvent(self, event):
        self.ui.lbl.setText(self.tr("Закрытие окна ..."))
        QApplication.processEvents()

        self._ensure_stop()
        self.reject()

    def _on_cancel(self):
        self.ui.lbl.setText(self.tr("Закрытие окна ..."))
        QApplication.processEvents()

        self._ensure_stop()
        self.reject()