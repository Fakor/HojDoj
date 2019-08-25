import tkinter as tk

from gui.sketch_gui import SketchGui
from gui.command_terminal import CommandTerminal


class MainWindow(tk.Frame):
    def __init__(self, parent, config, position, size):
        width, height = size
        tk.Frame.__init__(self, parent, width=width, height=height)
        self.parent = parent
        self.config = config
        self.position = position

        sketch_width = width
        sketch_height = int(height*0.95)

        self.parent.bind('<Control-c>', self.quit)
        self.place(x=0, y=0, width=sketch_width, height=height)
        self.sketch = SketchGui(self, config, position, size)
        self.sketch.place(x=0, y=0, width=sketch_width, height=sketch_height)

        command_width = width
        command_height = height - sketch_height
        self.command_terminal = CommandTerminal(self, self.sketch.get_command_table())

        self.command_terminal.place(x=0, y=sketch_height, width=command_width, height=command_height)

    def quit(self, event=None):
        self.parent.event_generate('<<quit_now>>')