import tkinter as tk
import code


class MainWindow(tk.Text):
    def __init__(self, parent, locals):
        self.parent = parent
        tk.Text.__init__(self, parent)

        self.grid()
        self.insert(0.0, ">>> ")

        self.shell = code.InteractiveInterpreter(locals=locals)