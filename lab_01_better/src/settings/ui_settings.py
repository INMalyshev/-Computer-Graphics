from src.settings.ui.button_settings import ButtonSettings
from src.settings.ui.canvas_settings import CanvasSettings
from src.settings.ui.dot_settings import DotSettings
from src.settings.ui.menu_settings import MenuSettings

class UiSettings:
    def __init__(self):
        self.button = ButtonSettings()
        self.canvas = CanvasSettings()
        self.dot = DotSettings()
        self.menu = MenuSettings()
