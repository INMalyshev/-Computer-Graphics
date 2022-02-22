from src.settings.math_settings import MathSettings
from src.settings.ui_settings import UiSettings

class Settings:
    def __init__(self):
        self.math = MathSettings()
        self.ui = UiSettings()

        self.approach = 1.1
        self.estange = 0.9

        self.move_len = 10
