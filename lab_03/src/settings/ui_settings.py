from src.settings.ui.canvas_settings import CanvasSettings
from src.settings.ui.menu_settings import MenuSettings
from src.settings.ui.button_settings import ButtonSettings

class UiSettings:
    def __init__(self):
        self.canvas = CanvasSettings()
        self.menu = MenuSettings()
        self.button = ButtonSettings()
