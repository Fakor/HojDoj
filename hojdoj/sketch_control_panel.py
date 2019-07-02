import tkinter as tk
import PIL

import sketch_interactive
from tools import elastic_background_horizontal, color_to_tk
import fillers
import image_button

B_WIDTH = 70
B_HEIGHT = 70

IMAGE_COLUMNS = 2
COLOR_COLUMNS = 2
ELASTIC_COLUMNS = 2


class SketchControlPanel(tk.Frame):
    def __init__(self, parent, sketch, config):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.sketch = sketch

        self.image_row = 1
        self.image_col = 0

        self.color_row = 7
        self.color_col = 0

        self.elastic_row = 12
        self.elastic_col = 0

        self.normal_images = []

        self.image_buttons = []

        self.p_images = []

        for template in config.image_templates:
            self.add_image_button(template)

        for color in config.sketch_colors:
            self.add_color_button(color)

        for elastic in config.image_elastics:
            self.add_elastic_image_button(elastic)

    def image_tool_active(self, image_meta):
        self.sketch.current_image = image_meta
        self.sketch.interactive_command = sketch_interactive.SketchInteractive

    def color_filler_active(self, color):
        self.sketch.filler = fillers.ColorFiller(self.sketch, color)
        for button in self.image_buttons:
            button.update()

    def elastic_image_filler_active(self, elastic_meta):
        self.sketch.filler = fillers.ElasticImageFiller(self.sketch, elastic_meta)
        for button in self.image_buttons:
            button.update()

    def add_image_button(self, path):
        button = image_button.ImageButton(self, path, (B_WIDTH, B_HEIGHT))
        self.image_buttons.append(button)
        button.grid(row=self.image_row, column=self.image_col)
        if self.image_col == IMAGE_COLUMNS - 1:
            self.image_col = 0
            self.image_row = self.image_row + 1
        else:
            self.image_col = self.image_col + 1

    def add_color_button(self, color):
        button = tk.Button(self, bg=color_to_tk(color), command=lambda: self.color_filler_active(color))
        button.grid(row=self.color_row, column=self.color_col)
        if self.color_col == COLOR_COLUMNS - 1:
            self.color_col = 0
            self.color_row = self.color_row + 1
        else:
            self.color_col = self.color_col + 1

    def add_elastic_image_button(self, elastic):
        path = elastic["path"]
        elastic_image = PIL.Image.open(path)
        image_button = elastic_background_horizontal(elastic_image, (B_WIDTH, B_HEIGHT))

        self.p_images.append(image_button)

        button = tk.Button(self,
                           image=self.p_images[-1],
                           command=lambda: self.elastic_image_filler_active(elastic))

        button.grid(row=self.elastic_row, column=self.elastic_col)
        if self.elastic_col == ELASTIC_COLUMNS - 1:
            self.elastic_col = 0
            self.elastic_row = self.elastic_row + 1
        else:
            self.elastic_col = self.elastic_col + 1
