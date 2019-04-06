import tkinter as tk


class Sketch(tk.Canvas):
    def __init__(self, parent, width, height):
        tk.Canvas.__init__(self, parent, width=width, height=height)
        self.pack()