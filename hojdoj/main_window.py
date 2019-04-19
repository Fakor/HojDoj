import tkinter as tk
import code


class MainWindow(tk.Text):
    def __init__(self, parent, loc):
        self.parent = parent
        tk.Text.__init__(self, parent)

        self.bind('<Control-c>', self.quit_app)

        self.grid()
        self.insert(0.0, ">>> ")

        self.shell = code.InteractiveInterpreter(locals=loc)

    def quit_app(self, event):
        self.parent.event_generate('<<quit_now>>')