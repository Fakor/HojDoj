import tkinter as tk
import PIL

import Commands
from tools import Colors, elastic_background
import fillers

B_WIDTH = 70
B_HEIGHT = 70

IMAGE_COLUMNS = 2
COLOR_COLUMNS = 2
ELASTIC_COLUMNS = 2


class SketchControlPanel(tk.Frame):
    def __init__(self, parent, sketch):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.sketch = sketch

        self.image_row = 1
        self.image_col = 0

        self.color_row = 7
        self.color_col = 0

        self.elastic_row = 10
        self.elastic_col = 0

        self.p_images = []

        self.add_image_button(self.sketch.image_paths.baltazar)
        self.add_image_button(self.sketch.image_paths.tummen)
        self.add_image_button(self.sketch.image_paths.door1)

        self.add_color_button(Colors.WHITE)
        self.add_color_button(Colors.BLACK)
        self.add_color_button(Colors.RED)
        self.add_color_button(Colors.BLUE)
        self.add_color_button(Colors.GREEN)

        self.add_elastic_image_button(self.sketch.image_paths.brick_wall)

        rect_button = tk.Button(self, text="Rectangle", command=self.rect_tool_active)

        rect_button.grid(row=0, column=0)

    def rect_tool_active(self):
        self.sketch.interactive_command = Commands.SketchRectInteractive

    def image_tool_active(self, path):
        self.sketch.current_image = path
        self.sketch.interactive_command = Commands.SketchImageInteractive

    def color_filler_active(self, color):
        self.sketch.filler = fillers.ColorFiller(self.sketch, color)

    def elastic_image_filler_active(self, path):
        self.sketch.filler = fillers.ElasticImageFiller(self.sketch, path)

    def add_image_button(self, path):
        img = PIL.Image.open(path)
        img = img.resize((B_WIDTH, B_HEIGHT), PIL.Image.ANTIALIAS)
        image_button = PIL.ImageTk.PhotoImage(img)
        self.p_images.append(image_button)
        button = tk.Button(self, image=self.p_images[-1],
                           command=lambda: self.image_tool_active(path),
                           height=B_HEIGHT, width=B_WIDTH)
        button.grid(row=self.image_row, column=self.image_col)
        if self.image_col == IMAGE_COLUMNS - 1:
            self.image_col = 0
            self.image_row = self.image_row + 1
        else:
            self.image_col = self.image_col + 1

    def add_color_button(self, color):
        button = tk.Button(self, bg=color['tk'], command=lambda: self.color_filler_active(color))
        button.grid(row=self.color_row, column=self.color_col)
        if self.color_col == COLOR_COLUMNS - 1:
            self.color_col = 0
            self.color_row = self.color_row + 1
        else:
            self.color_col = self.color_col + 1

    def add_elastic_image_button(self, path):
        image_button = elastic_background(path, (B_WIDTH, B_HEIGHT))

        self.p_images.append(image_button)

        button = tk.Button(self, image=self.p_images[-1], command=lambda: self.elastic_image_filler_active(path))

        button.grid(row=self.elastic_row, column=self.elastic_col)
        if self.elastic_col == ELASTIC_COLUMNS - 1:
            self.elastic_col = 0
            self.elastic_row = self.elastic_row + 1
        else:
            self.elastic_col = self.elastic_col + 1
