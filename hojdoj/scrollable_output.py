import tkinter as tk

COMMAND = 'command'


class ScrollableOutput(tk.Text):
    def __init__(self, parent):
        self.parent = parent
        tk.Text.__init__(self, parent)
        self.insert(tk.END, "HojDoj Scrollable output")
        self.tag_configure(COMMAND, foreground='green')

    def add_command(self, text):
        self.insert(tk.END, '\n' + text, COMMAND)


class NormalOutput:
    def add_command(self, text):
        print(text)