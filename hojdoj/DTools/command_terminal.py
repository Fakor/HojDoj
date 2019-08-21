import tkinter as tk
import code
from DTools.tools import value_to_string


def command(output):
    def base_call(func):
        def wrapper(*args, **kwargs):
            output.print_command(func, *args, **kwargs)
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

    def print_command(self, command):
        text = "{}(".format(command.name)
        text += ', '.join(['{}={}'.format(str(key),value_to_string(value)) for key, value in command.get_kwargs().items() if value is not None])

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

    def add_local(self, name, value):
        self.shell.locals[name] = value

