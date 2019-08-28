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
    def __init__(self, parent, command_table, width, height):
        tk.Frame.__init__(self, parent)
        self.input = InputEntry(self)
        self.input.place(width=width, height=height)

        self.interpreter = Interpreter(command_table)

    def run_command(self, text, update_text=False):
        self.interpreter.perform_command(text)
        if update_text:
            self.input.delete(0, tk.END)
            self.input.insert(0, text)
