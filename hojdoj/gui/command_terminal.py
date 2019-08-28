import tkinter as tk

from logic.interpreter import Interpreter


class InputEntry(tk.Entry):
    def __init__(self, parent):
        tk.Entry.__init__(self, parent)
        self.parent = parent
        self.bind('<Return>', self.enter_pressed)

    def enter_pressed(self, event):
        self.parent.run_command(self.get())


class CommandTerminal(tk.Frame):
    def __init__(self, parent, command_table):
        tk.Frame.__init__(self, parent)
        self.input = InputEntry(self)
        self.input.grid()

        self.interpreter = Interpreter(command_table)

    def run_command(self, text):
        self.interpreter.perform_command(text)
