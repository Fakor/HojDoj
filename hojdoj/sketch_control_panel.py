import tkinter as tk
import PIL

import Commands

B_WIDTH = 70
B_HEIGHT = 70

COLUMNS = 2


class SketchControlPanel(tk.Frame):
    def __init__(self, parent, sketch):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.sketch = sketch

        self.image_row = 1
        self.image_col = 0

        self.p_images = []

        self.add_image_button(self.sketch.image_paths.baltazar)
        self.add_image_button(self.sketch.image_paths.tummen)
        self.add_image_button(self.sketch.image_paths.door1)

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

    def image_tool_active(self, path):
        self.sketch.current_image = path
        self.sketch.interactive_command = Commands.SketchImageInteractive

    def color_blue_active(self):
        self.sketch.fill_color = "blue"

    def color_red_active(self):
        self.sketch.fill_color = "red"

    def add_image_button(self, path):
        img = PIL.Image.open(path)
        img = img.resize((B_WIDTH, B_HEIGHT), PIL.Image.ANTIALIAS)
        image_button = PIL.ImageTk.PhotoImage(img)
        self.p_images.append(image_button)
        button = tk.Button(self, image=self.p_images[-1],
                                command=lambda: self.image_tool_active(path),
                                height=B_HEIGHT, width=B_WIDTH)
        button.grid(row=self.image_row, column=self.image_col)
        if self.image_col == COLUMNS - 1:
            self.image_col = 0
            self.image_row = self.image_row + 1
        else:
            self.image_col = self.image_col + 1

