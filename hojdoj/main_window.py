import tkinter as tk

from Sketch import Sketch


class MainWindow(tk.Text):
    def __init__(self, parent):
        self.parent = parent
        tk.Text.__init__(self, parent)
        self.bind('<Return>', self.enter_pressed)

        self.grid()
        self.insert(0.0, ">>> ")

        self.sketch_window = tk.Toplevel(self.parent)
        self.sketch = Sketch(self.sketch_window, 300, 300)
        self.sketch.grid()

        self.label_window = tk.Toplevel(self.parent)
        self.text = tk.StringVar()

        self.label = tk.Label(self.sketch_window, textvariable=self.text)
        self.text.set("Not set yet")
        self.label.grid()

    def enter_pressed(self, event):
        exec(self.get(1.4, tk.END))