import tkinter as tk

class CommandWindow(tk.Text):
    def __init__(self, parent):
        tk.Text.__init__(self, parent)

        self.grid()
        self.insert(0.0, ">>> ")
