import tkinter as tk


class SketchControlPanel(tk.Frame):
    def __init__(self, parent, sketch):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.sketch = sketch

        line_button = tk.Button(self, text="Line", command=self.line_tool_active)
        line_button.grid(row=0, column=0)
        rect_button = tk.Button(self, text="Rectangle", command=self.rect_tool_active)
        rect_button.grid(row=0, column=1)

    def line_tool_active(self):
        self.sketch.paint_command = "line"

    def rect_tool_active(self):
        self.sketch.paint_command = "rect"
