import tkinter as tk
import PIL

import Commands

B_WIDTH = 70
B_HEIGHT = 70


class SketchControlPanel(tk.Frame):
    def __init__(self, parent, sketch):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.sketch = sketch

        self.balt_img = PIL.Image.open(self.sketch.image_paths.baltazar)
        self.balt_img = self.balt_img.resize((B_WIDTH, B_HEIGHT), PIL.Image.ANTIALIAS)
        self.balt_image_button = PIL.ImageTk.PhotoImage(self.balt_img)

        line_button = tk.Button(self, text="Line", command=self.line_tool_active)
        rect_button = tk.Button(self, text="Rectangle", command=self.rect_tool_active)
        balt_button = tk.Button(self, image=self.balt_image_button,
                                command=self.image_tool_active,
                                height=B_HEIGHT, width=B_WIDTH)

        line_button.grid(row=0, column=0)
        rect_button.grid(row=0, column=1)
        balt_button.grid(row=1, column=0)

        blue_button = tk.Button(self, bg="blue", command=self.color_blue_active)
        red_button = tk.Button(self, bg="red", command=self.color_red_active)

        blue_button.grid(row = 3, column=0)
        red_button.grid(row=3, column=1)

    def line_tool_active(self):
        self.sketch.interactive_command = Commands.SketchLineInteractive

    def rect_tool_active(self):
        self.sketch.interactive_command = Commands.SketchRectInteractive

    def image_tool_active(self):
        self.sketch.interactive_command = Commands.SketchImageInteractive

    def color_blue_active(self):
        self.sketch.fill_color = "blue"

    def color_red_active(self):
        self.sketch.fill_color = "red"