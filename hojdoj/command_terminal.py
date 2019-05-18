import tkinter as tk
import code
import sys

STDOUT = 'stdout'
STDERR = 'stderr'


class IORedirector:

    def __init__(self, out_func):
        self.out_func = out_func

    def write(self, str):
        self.out_func(str)

    def flush(self):
        pass


class CommandTerminal(tk.Text):

    ROW_START = ">>> "

    def __init__(self, parent, loc):
        self.parent = parent
        tk.Text.__init__(self, parent)

        self.tag_configure(STDOUT, foreground='blue')
        self.tag_configure(STDERR, foreground='red')

        self.bind('<Control-c>', self.quit_app)
        self.bind('<Return>', self.enter_pressed)

        self.insert(0.0, self.ROW_START)

        self.shell = code.InteractiveInterpreter(locals=loc)

    def quit_app(self, event):
        self.parent.event_generate('<<quit_now>>')

    def set_as_console(self):
        sys.stderr = IORedirector(self.add_stderr)
        sys.stdout = IORedirector(self.add_stdout)

    def enter_pressed(self, event):
        row = int(self.index(tk.END).split('.')[0])-1
        pos = "{}.{}".format(row, len(self.ROW_START))
        line_private___ = self.get(pos, tk.END).strip()
        if len(line_private___) == 0:
            pass
        elif line_private___[-1] != ":":
            self.shell.runcode(line_private___)
        self.insert(tk.END, '\n{}'.format(self.ROW_START))
        self.mark_set("insert", tk.END)
        return 'break'

    def add_stdout(self, text):
        self.insert(tk.END, '\n' + text.strip(), STDOUT)

    def add_stderr(self, text):
        self.insert(tk.END, '\n' + text.strip(), STDERR)
