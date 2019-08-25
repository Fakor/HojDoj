import tkinter as tk

from gui.sketch_gui import SketchGui


class MainWindow(tk.Frame):
    def __init__(self, parent, config, position, size):
        width, height = size
        tk.Frame.__init__(self, parent, width=width, height=height)
        self.parent = parent
        self.config = config
        self.position = position

        self.parent.bind('<Control-c>', self.quit)
        self.place(x=0, y=0, width=width, height=height)
        self.sketch = SketchGui(self, config, position, size)
        self.sketch.place(x=0, y=0, width=width, height=height)

    def quit(self, event=None):
        self.parent.event_generate('<<quit_now>>')