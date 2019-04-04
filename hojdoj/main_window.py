import tkinter as tk

from command_window import CommandWindow


class MainWindow:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(self.parent)

        self.text_var = tk.StringVar()

        self.label = tk.Label(self.frame, textvariable = self.text_var)
        self.text_var.set("Not set yet")
        self.label.pack()

        v = {
            'text_var': self.text_var
        }

        self.new_window = tk.Toplevel(self.parent)
        self.command = CommandWindow(self.new_window, v)
        self.frame.pack()
        self.new_window.pack_slaves()