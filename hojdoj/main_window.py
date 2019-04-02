import tkinter as tk

import interpreter


class MainWindow:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent)

        self.interpreter = interpreter.Console(self.parent)
        self.new_window = tk.Toplevel(self.parent)

        self.frame.pack()