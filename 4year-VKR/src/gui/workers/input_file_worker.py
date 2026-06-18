from PySide6.QtCore import QObject, Signal, QThread

from core.io import read_data, read_data_writable

class InputFileWorker(QObject):
    data_loaded = Signal(object)
    error_occurred = Signal(str)
    finished = Signal()

    def __init__(self, file_path: str, max_rows: int | None = None, read_writable: bool = False):
        super().__init__()
        self.file_path = file_path
        self.max_rows = max_rows
        self.read_writable = read_writable

    def run_task(self):
        try:
            if self.read_writable:
                data = read_data_writable(self.file_path, max_rows=self.max_rows, n_chunk_rows=100_000)
            else:
                data = read_data(self.file_path, max_rows=self.max_rows)
            self.data_loaded.emit(data)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.finished.emit()