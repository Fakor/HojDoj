import tkinter as tk

from command_window import CommandWindow
from Scetch import Scetch


class MainWindow:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent)

        self.text_var = tk.StringVar()

        self.label = tk.Label(self.frame, textvariable = self.text_var)
        self.text_var.set("Not set yet")
        self.label.pack()


        self.scetch_window = tk.Toplevel(self.parent)
        self.scetch = Scetch(self.scetch_window, 300, 300)

        v = {
            'text_var': self.text_var,
            'scetch': self.scetch
        }

        self.command_window = tk.Toplevel(self.parent)
        self.command = CommandWindow(self.command_window, v)

        self.frame.pack()