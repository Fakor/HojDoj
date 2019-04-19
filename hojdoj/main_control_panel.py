import tkinter as tk


class MainControlPanel(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.root = root
        quit_button = tk.Button(self, text="Quit", command=self.quit_app)
        quit_button.grid()

    def quit_app(self):
        self.root.event_generate('<<quit_now>>')