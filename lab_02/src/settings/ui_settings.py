from src.settings.ui.canvas_settings import CanvasSettings
from src.settings.ui.menu_settings import MenuSettings

class UiSettings:
    def __init__(self):
        self.canvas = CanvasSettings()
        self.menu = MenuSettings()
