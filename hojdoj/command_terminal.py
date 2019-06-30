import tkinter as tk
import code
from tools import value_to_string


def command(output):
    def base_call(func):
        def wrapper(*args, **kwargs):
            output.add_command(func, *args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return base_call


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

    def add_command(self, func, *args, **kwargs):
        text = "{}(".format(func.__name__)
        if len(args) > 0:
            text = text + value_to_string(args[0])
            for arg in args[1:]:
                text = text + ',' + value_to_string(arg)
        if len(kwargs) > 0:
            first_done = False
            for key, value in kwargs.items():
                if not first_done and len(args) == 0:
                    text = text + str(key) + '=' + value_to_string(value)
                else:
                    text = text + ',' + str(key) + '=' + value_to_string(value)
        text = text + ")"

        self.input.delete(0, tk.END)
        self.input.insert(0, text)

    def enter_pressed(self, event):
        self.shell.runcode(self.input.get())

    def place(self, **kwargs):
        self.input.config(width=int(kwargs["width"]))
        tk.Frame.place(self, **kwargs)

    def run_command(self, text):
        self.shell.runcode(text)

