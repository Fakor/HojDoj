import tkinter as tk
import code


class InputEntry(tk.Entry):
    def __init__(self, parent):
        tk.Entry.__init__(self, parent)
        self.parent = parent
        self.bind('<Return>', self.enter_pressed)

    def enter_pressed(self, event):
        self.parent.run_command(self.get())


class CommandTerminal(tk.Frame):
    def __init__(self, parent, loc):
        tk.Frame.__init__(self, parent)
        self.input = InputEntry(self)

        self.input.grid(row=0,column=0)

        self.shell = code.InteractiveInterpreter(locals=loc)

    def add_command(self, text):
        self.input.delete(0, tk.END)
        self.input.insert(0, text)

    def enter_pressed(self, event):
        self.shell.runcode(self.input.get())

    def place(self, **kwargs):
        self.input.config(width=int(kwargs["width"]))
        tk.Frame.place(self, **kwargs)

    def run_command(self, text):
        self.shell.runcode(text)