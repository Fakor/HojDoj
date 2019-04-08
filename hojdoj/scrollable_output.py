import tkinter as tk


class ScrollableOutput(tk.Label):
    def __init__(self, parent):
        self.parent = parent
        tk.Label.__init__(self, parent)

        self.config(text="HojDoj Scrollable output")