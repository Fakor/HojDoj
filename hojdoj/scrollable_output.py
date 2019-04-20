import tkinter as tk

import sys


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

    def add_command(self, text):
        self.insert(tk.END, '\n' + text)

    def add_stdout(self, text):
        self.insert(tk.END, '\n' + text)

    def add_stderr(self, text):
        self.insert(tk.END, '\n' + text)
