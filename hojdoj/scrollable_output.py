import tkinter as tk

import sys


COMMAND = 'command'
STDOUT = 'stdout'
STDERR = 'stderr'


class IORedirector:

    def __init__(self, out_func):
        self.out_func = out_func

    def write(self, str):
        self.out_func(str)

    def flush(self):
        pass


class ScrollableOutput(tk.Text):
    def __init__(self, parent):
        self.parent = parent
        tk.Text.__init__(self, parent)
        self.insert(tk.END, "HojDoj Scrollable output")
        sys.stderr = IORedirector(self.add_stderr)
        sys.stdout = IORedirector(self.add_stdout)
        self.tag_configure(COMMAND, foreground='green')
        self.tag_configure(STDOUT, foreground='blue')
        self.tag_configure(STDERR, foreground='red')

    def add_command(self, text):
        self.insert(tk.END, '\n' + text, COMMAND)

    def add_stdout(self, text):
        self.insert(tk.END, '\n' + text.strip(), STDOUT)

    def add_stderr(self, text):
        self.insert(tk.END, '\n' + text, STDERR)
