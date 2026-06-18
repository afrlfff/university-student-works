import numpy as np
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox
from PySide6.QtCore import Signal, QFileInfo
from gui.ui_autogen.ui_shottky_search_panel import Ui_ShottkySearchPanel

from gui.core.settings_storage import SettingsStorage
from gui.panels.base_panel import BasePanel
from core.types import AppState
from gui.dialogs.get_shottky_params_dialog import GetShottkyParamsDialog

class ShottkySearchPanel(BasePanel):
    search_started = Signal()
    search_finished = Signal()
    search_failed = Signal()

    def __init__(self, parent=None, app_state: AppState = None):
        super().__init__(parent, app_state)
        self.ui = Ui_ShottkySearchPanel()
        self.ui.setupUi(self)

        self.ui.btn_run.clicked.connect(self._on_run)
        self.ui.btn_import.clicked.connect(self.import_data)
        
        self.sync()

    def sync(self):
        valid = self._app_state.is_source_data_valid()

        self.ui.btn_run.setEnabled(self._app_state.shottky_params.size == 0)
        self.ui.btn_import.setEnabled(valid)

    def _on_run(self):
        self._app_state.shottky_params = np.array([])
        shottky_search_dialog = GetShottkyParamsDialog(self._app_state, parent=self)
        self.search_started.emit()

        if shottky_search_dialog.exec() == QDialog.DialogCode.Accepted:
            self._app_state.shottky_params = shottky_search_dialog.get_params()
            self.search_finished.emit()
        else:
            self.search_failed.emit()
    
    def import_data(self):
        default_dir = SettingsStorage.get("import/shottky_params_dir", "")
        default_path = default_dir if default_dir else ""

        path, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Импорт параметров Шоттки"),
            default_path,
            self.tr("Text files (*.txt);;All files (*)"),
        )

        if not path:
            return

        params = self._read_shottky_params_file(path)
        expected_rows = self._app_state.last_cycle_idx - self._app_state.first_cycle_idx + 1

        if params is None:
            QMessageBox.warning(
                self,
                self.tr("Ошибка импорта"),
                self.tr("Файл не соответствует формату: в каждой непустой строке должно быть 5 чисел."),
            )
            return

        if params.shape != (expected_rows, 5):
            QMessageBox.warning(
                self,
                self.tr("Ошибка импорта"),
                self.tr(
                    f"Некорректное количество строк.\n"
                    f"Ожидалось: {expected_rows}\n"
                    f"Получено: {params.shape[0]}"
                ),
            )
            return

        import_dir = QFileInfo(path).absolutePath()
        SettingsStorage.set("import/shottky_params_dir", import_dir)
        SettingsStorage.sync()

        self._app_state.shottky_params = params

        self.sync()
        self.search_finished.emit()

    def _read_shottky_params_file(self, path: str) -> np.ndarray | None:
        rows = []

        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    # пустые строки, включая пустую строку в конце файла, игнорируем
                    if not line:
                        continue

                    parts = line.split()

                    if len(parts) != 5:
                        return None

                    try:
                        row = [float(x.replace(",", ".")) for x in parts]
                    except ValueError:
                        return None

                    rows.append(row)

        except OSError:
            return None

        if not rows:
            return None

        return np.asarray(rows, dtype=float)