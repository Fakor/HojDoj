import tkinter as tk


class MainControlPanel(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.root = root
        undo_button = tk.Button(self, text="Undo", command=self.sketch_undo)
        redo_button = tk.Button(self, text="Redo", command=self.sketch_redo)
        quit_button = tk.Button(self, text="Quit", command=self.quit_app)

        undo_button.grid(row=0, column=0)
        redo_button.grid(row=0, column=1)

        quit_button.grid(row=3, column=0)

    def quit_app(self):
        self.root.event_generate('<<quit_now>>')

    def sketch_undo(self):
        self.parent.sk.undo()

    def sketch_redo(self):
        self.parent.sk.redo()