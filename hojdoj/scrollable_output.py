import tkinter as tk


class ScrollableOutput(tk.Text):
    def __init__(self, parent):
        self.parent = parent
        tk.Text.__init__(self, parent)
        self.insert(tk.END, "HojDoj Scrollable output")

    def add_row(self, new_row):
        self.insert(tk.END, '\n' + new_row)