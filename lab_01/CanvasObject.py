import tkinter

import Settings

class CanvasObject(tkinter.Canvas):
    def __init__(self, root):
        self.settings = Settings.Settings()

        geometry = self.settings.geometry
        geometry = geometry.replace('+', 'x')
        data = geometry.split('x')
        width = int(int(data[0]) * self.settings.canvasWidthReference)
        height = int(int(data[1]) * self.settings.canvasHeightReference)

        super(CanvasObject, self).__init__(root, width=width, height=height, bg=self.settings.fieldcolor)
        self.bind("<MouseWheel>", self.zoom)

    def rewind(self):
        self.delete(self.settings.useritemtag)
        self.delete(self.settings.solutiontag)

    def zoom(self, event):
        if (event.delta > 0):
            self.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.scale("all", event.x, event.y, 0.9, 0.9)
