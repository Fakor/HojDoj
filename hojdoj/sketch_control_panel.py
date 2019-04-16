import tkinter as tk

import Commands

class SketchControlPanel(tk.Frame):
    def __init__(self, parent, sketch):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.sketch = sketch

        line_button = tk.Button(self, text="Line", command=self.line_tool_active)
        rect_button = tk.Button(self, text="Rectangle", command=self.rect_tool_active)

        line_button.grid(row=0, column=0)
        rect_button.grid(row=0, column=1)

        blue_button = tk.Button(self, bg="blue", command=self.color_blue_active)
        red_button = tk.Button(self, bg="red", command=self.color_red_active)

        blue_button.grid(row = 3, column=0)
        red_button.grid(row=3, column=1)

    def line_tool_active(self):
        self.sketch.interactive_command = Commands.SketchLineInteractive

    def rect_tool_active(self):
        self.sketch.interactive_command = Commands.SketchRectInteractive

    def color_blue_active(self):
        self.sketch.fill_color = "blue"

    def color_red_active(self):
        self.sketch.fill_color = "red"