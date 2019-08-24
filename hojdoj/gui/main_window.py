import tkinter as tk


class MainWindow(tk.Frame):
    def __init__(self, parent, config, position, size):
        tk.Frame.__init__(self, parent, width=size[0], height=size[1])
        self.parent = parent
        self.config = config
        self.position = position

        self.parent.bind('<Control-c>', self.quit)
        self.place(x=position[0], y=position[1], width=size[0], height=size[1])

    def quit(self, event=None):
        self.parent.event_generate('<<quit_now>>')