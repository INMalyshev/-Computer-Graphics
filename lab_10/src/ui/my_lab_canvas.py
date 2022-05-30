from src.ui.my_canvas import MyCanvas
from src.field import Field
from src.vector import Vector


class MyLabCanvas(MyCanvas):
    def __init__(self, parent):
        super(MyLabCanvas, self).__init__(parent)

    def set_position(self, data,  **kwargs):
        self.delete("all")
        self.draw_cross()
