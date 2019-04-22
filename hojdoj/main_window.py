import tkinter as tk
import code


class MainWindow(tk.Text):

    ROW_START = ">>> "

    def __init__(self, parent, loc):
        self.parent = parent
        tk.Text.__init__(self, parent)

        self.bind('<Control-c>', self.quit_app)
        self.bind('<Return>', self.enter_pressed)

        self.grid()
        self.insert(0.0, self.ROW_START)

        self.shell = code.InteractiveInterpreter(locals=loc)

    def quit_app(self, event):
        self.parent.event_generate('<<quit_now>>')

    def enter_pressed(self, event):
        row = int(self.index(tk.END).split('.')[0])-1
        pos = "{}.{}".format(row, len(self.ROW_START))
        line_private___ = self.get(pos, tk.END).strip()
        if line_private___[-1] != ":":
            self.shell.runcode(line_private___)
        self.insert(tk.END, '\n{}'.format(self.ROW_START))
        return 'break'