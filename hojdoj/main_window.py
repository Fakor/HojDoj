import tkinter as tk
import code


class MainWindow(tk.Text):
    def __init__(self, parent, loc):
        self.parent = parent
        tk.Text.__init__(self, parent)

        self.bind('<Control-c>', self.quit_app)
        self.bind('<Return>', self.enter_pressed)

        self.grid()
        self.insert(0.0, ">>> ")

        self.shell = code.InteractiveInterpreter(locals=loc)

    def quit_app(self, event):
        self.parent.event_generate('<<quit_now>>')

    def enter_pressed(self, event):
        line_private___ = self.get(1.4, tk.END).strip()
        if line_private___[-1] != ":":
            self.shell.runcode(line_private___)