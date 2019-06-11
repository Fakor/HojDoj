import tkinter as tk
import code


class InputEntry(tk.Entry):
    def __init__(self, parent):
        tk.Entry.__init__(self, parent)
        self.parent = parent
        self.bind('<Return>', self.enter_pressed)

    def enter_pressed(self, event):
        self.parent.run_command(self.get())
        self.delete(0,tk.END)


class CommandTerminal(tk.Frame):
    def __init__(self, parent, loc):
        tk.Frame.__init__(self, parent)
        self.content = tk.StringVar()
        self.input = InputEntry(self)
        self.output = tk.Entry(self, textvariable=self.content)

        self.input.grid(row=0,column=0)
        self.output.grid(row=1,column=0)

        self.shell = code.InteractiveInterpreter(locals=loc)

    def add_command(self, text):
        self.content.set(text)

    def run_command(self, text):
        self.shell.runcode(text)

    def place(self, **kwargs):
        self.output.config(width=int(kwargs["width"]/2))

        self.input.config(width=int(kwargs["width"] / 2))

        tk.Frame.place(self, **kwargs)
