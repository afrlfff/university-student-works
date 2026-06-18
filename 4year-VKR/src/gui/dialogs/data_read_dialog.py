import numpy as np
from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtCore import QThread, Qt, QTimer
from gui.ui_autogen.ui_data_read_dialog import Ui_DataReadDialog

from gui.workers.input_file_worker import InputFileWorker
from core.io import count_rows
from core.algorithms import find_stable_zeros, find_extrema, estimate_frequency_fft, get_num_periods, get_period_indices

class DataReadDialog(QDialog):
    def __init__(self, path_to_Vin: str, path_to_Vout: str, R: int, dt: float, parent=None):
        super().__init__(parent)
        self.ui = Ui_DataReadDialog()
        self.ui.setupUi(self)

        self._path_to_Vin = path_to_Vin
        self._path_to_Vout = path_to_Vout
        self._threads = set()
        self._workers = set()
        self._n_read_files = 0
        self._success = False
        self._closing = False

        self._V = np.array([])
        self._I = np.array([])
        self._R = R
        self._dt = dt
        self._Vzeros = np.array([])
        self._Vmaxima = np.array([])
        self._Vminima = np.array([])
        self._V_freq = 1.0

        self.ui.lbl.setText(self.tr("Чтение файлов ..."))

        self.ui.btn_close.clicked.connect(self._on_cancel)

        # self._init_reading()
        QTimer.singleShot(0, self._init_reading)

    def _init_reading(self):
        file1_rows = count_rows(self._path_to_Vin)
        file2_rows = count_rows(self._path_to_Vout)
        max_rows = min(file1_rows, file2_rows)

        for path, on_loaded, read_writable in [
            (self._path_to_Vin, self._on_Vin_loaded, False),
            (self._path_to_Vout, self._on_Vout_loaded, True)
        ]:
            worker = InputFileWorker(path, max_rows=max_rows, read_writable=read_writable)
            thread = QThread()
            worker.moveToThread(thread)

            # Гарантируем выполнение в worker-потоке, а не в GUI
            thread.started.connect(worker.run_task, Qt.QueuedConnection)
            worker.data_loaded.connect(on_loaded, Qt.QueuedConnection)
            worker.error_occurred.connect(lambda err, p=path: self._on_error(p, err), Qt.QueuedConnection)
            
            # Безопасная цепочка завершения
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

    def _on_Vin_loaded(self, Vin):
        self._V = Vin
        self._n_read_files += 1

        if self._n_read_files == 2:
            self._success = self._calculate_additional_data()

            if self._success:
                self.ui.lbl.setText(self.tr("Данные успешно прочитаны."))
            else:
                self.ui.lbl.setText(self.tr("Ошибка индексации данных. Программа не сможет их обработать."))
            self.ui.btn_close.setText(self.tr("Ок"))

    def _on_Vout_loaded(self, Vout):
        self._I = Vout
        self._I /= self._R
        self._n_read_files += 1

        if self._n_read_files == 2:
            self._success = self._calculate_additional_data()

            if self._success:
                self.ui.lbl.setText(self.tr("Данные успешно прочитаны."))
            else:
                self.ui.lbl.setText(self.tr("Ошибка индексации данных. Программа не сможет их обработать."))
            self.ui.btn_close.setText(self.tr("Ок"))

    def _calculate_additional_data(self):
        self.ui.lbl.setText(self.tr("Индексация данных ..."))
        QApplication.processEvents()

        try:
            # get main freqency assuming at least 1 period fits in 10e6 points
            self._V_freq = estimate_frequency_fft(self._V[:1_000_000], self._dt)
            period_s = 1 / self._V_freq
            period_samples = round(period_s / self._dt)

            # calculate zeros
            min_distance = int(round(period_samples / 6))
            self._Vzeros = find_stable_zeros(self._V, min_distance=min_distance)
            if self._Vzeros.size > 0 and self._Vzeros[0] > 0:
                self._Vzeros = np.concatenate([[0], self._Vzeros])
            
            # calculate maxima and minima
            num_cycles = get_num_periods(self._Vzeros, segments_per_period=2)
            self._Vmaxima = np.empty(num_cycles, dtype=int)
            self._Vminima = np.empty(num_cycles, dtype=int)
            for i in range(num_cycles):
                start, end = get_period_indices(self._V.size, i, self._Vzeros, segments_per_period=2, period_start_segment_idx=0)
                V = self._V[start : end + 1]

                window = max(3, int(0.01 * V.size))
                min_idx, max_idx = find_extrema(V, smooth=True, smooth_window=window, smooth_mode='wrap')

                self._Vminima[i] = start + min_idx
                self._Vmaxima[i] = start + max_idx

            # success finish            
            return True

        except Exception:
            return False

    def _on_error(self, file_path: str, erorr_msg: str):
        self.ui.lbl.setText(self.tr("Ошибка при чтении файла: ") + f"{file_path}")
        self.ui.btn_close.setText(self.tr("Ок"))
        self._request_shutdown()

    def get_V(self):
        return self._V
    
    def get_I(self):
        return self._I
    
    def get_Vzeros(self):
        return self._Vzeros
    
    def get_Vmaxima(self):
        return self._Vmaxima
    
    def get_Vminima(self):
        return self._Vminima
    
    def get_V_freq(self):
        return self._V_freq

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
        self._close()
        # self.accept()

    def _on_cancel(self):
        self._close()
        # self.accept()

    def _close(self):
        if self._closing:
            return

        self._closing = True

        self.ui.lbl.setText(self.tr("Закрытие окна ..."))
        QApplication.processEvents()

        self._ensure_stop()
        if self._success:
            self.accept()
        else:
            self.reject()