import tkinter as tk

import sketch_image_tool


class MainControlPanel(tk.Frame):
    def __init__(self, parent, root, sketch):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.root = root
        self.sketch = sketch

        quit_button = tk.Button(self, text="Quit", command=self.quit_app)
        undo_button = tk.Button(self, text="Undo", command=self.sketch_undo)
        redo_button = tk.Button(self, text="Redo", command=self.sketch_redo)
        sketch_button = tk.Button(self, text="Sketch", command=self.interactive_sketch)

        quit_button.grid(row=0, column=0)
        undo_button.grid(row=1, column=0)
        redo_button.grid(row=2, column=0)
        sketch_button.grid(row=3, column=0)

    def quit_app(self):
        self.root.event_generate('<<quit_now>>')

    def sketch_undo(self):
        self.sketch.undo_command(it=1)

    def sketch_redo(self):
        self.sketch.redo_command(it=1)

    def interactive_sketch(self):
        self.sketch.interactive_command = sketch_image_tool.SketchImageTool