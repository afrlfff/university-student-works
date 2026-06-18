from PySide6.QtWidgets import QWidget
from core.types import AppState

class BasePanel(QWidget):
    def __init__(self, parent=None, app_state: AppState | None = None):
        super().__init__(parent)

        self._app_state = app_state if app_state else AppState()

    def sync(self) -> None:
        raise NotImplementedError