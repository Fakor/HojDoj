import tkinter as tk
import code

from sketch import Sketch
from scrollable_output import ScrollableOutput


class MainWindow(tk.Text):
    def __init__(self, parent):
        self.parent = parent
        tk.Text.__init__(self, parent)
        self.bind('<Return>', self.enter_pressed)
        self.bind('<Control-c>', self.quit)

        self.grid()
        self.insert(0.0, ">>> ")

        self.sketch_window = tk.Toplevel(self.parent)
        self.sketch = Sketch(self.sketch_window, 300, 300)
        self.sketch.grid()

        self.output_window = tk.Toplevel(self.parent)
        self.output = ScrollableOutput(self.output_window)
        self.output.grid()

        self.shell = code.InteractiveInterpreter(locals=locals())

    def enter_pressed(self, event):
        line_private___ = self.get(1.4, tk.END).strip()
        if line_private___[-1] != ":":
            self.shell.runcode(line_private___)

    def quit(self, event):
        self.parent.quit()