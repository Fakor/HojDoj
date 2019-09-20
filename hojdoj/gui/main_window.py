import tkinter as tk

from gui.sketch_gui import SketchGui
from gui.command_terminal import CommandTerminal
from DTools.tools import value_to_string


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
        command_width = width
        command_height = height - sketch_height
        self.command_terminal = CommandTerminal(self, command_width, command_height)

        self.sketch = SketchGui(self, config, position, (sketch_width, sketch_height), self.command_terminal)
        self.sketch.place(x=0, y=0, width=sketch_width, height=sketch_height)

        self.command_terminal.set_command_table(self.sketch.get_command_table())

        self.command_terminal.place(x=0, y=sketch_height, width=command_width, height=command_height)

    def quit(self, event=None):
        self.parent.event_generate('<<quit_now>>')

    def new_command(self, command_name, *args, **kwargs):
        text = "{}(".format(command_name)

        args_text = [value_to_string(arg) for arg in args]
        kwargs_text =['{}={}'.format(str(key),value_to_string(value)) for key, value in kwargs.items() if value is not None]
        text = text + ', '.join(args_text  + kwargs_text) + ")"

        self.command_terminal.run_command(text, update_text=True)