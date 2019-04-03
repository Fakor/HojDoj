import tkinter as tk


class CommandWindow(tk.Text):
    def __init__(self, parent, text_var):
        tk.Text.__init__(self, parent)
        self.text_var = text_var

        self.bind('<Return>', self.enter_pressed)
        self.grid()
        self.insert(0.0, ">>> ")

    def enter_pressed(self, event):
        self.text_var.set(self.get(1.4, tk.END))
