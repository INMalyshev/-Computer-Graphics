from src.settings.ui.button_settings import ButtonSettings
from src.settings.ui.canvas_settings import CanvasSettings

class UiSettings:
    def __init__(self):
        self.button = ButtonSettings()
        self.canvas = CanvasSettings()
