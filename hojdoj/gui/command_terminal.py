import tkinter as tk


class InputEntry(tk.Entry):
    def __init__(self, parent):
        tk.Entry.__init__(self, parent)
        self.parent = parent
        self.bind('<Return>', self.enter_pressed)

    def enter_pressed(self, event):
        self.parent.callback(self.get())


class CommandTerminal(tk.Frame):
    def __init__(self, parent, width, height, interpreter):
        tk.Frame.__init__(self, parent)
        self.input = InputEntry(self)
        self.input.place(width=width, height=height)

        interpreter.callback = self.update_text
        self.callback = interpreter.perform_command

    def update_text(self, text):
        self.input.delete(0, tk.END)
        self.input.insert(0, text)
