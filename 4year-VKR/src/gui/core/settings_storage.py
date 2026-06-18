from PySide6.QtCore import QSettings

class SettingsStorage:
    _settings = QSettings("frlfff", "Memristor Identification App")

    @classmethod
    def get(cls, key: str, default=None):
        val = cls._settings.value(key)
        return val if val is not None else default

    @classmethod
    def set(cls, key: str, value):
        cls._settings.setValue(key, value)

    @classmethod
    def sync(cls):
        cls._settings.sync()