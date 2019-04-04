import tkinter as tk


class CommandWindow(tk.Text):
    def __init__(self, parent, v):
        tk.Text.__init__(self, parent)
        self.v = v

        self.bind('<Return>', self.enter_pressed)
        self.grid()
        self.insert(0.0, ">>> ")

    def enter_pressed(self, event):
        exec(self.get(1.4, tk.END))
