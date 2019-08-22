import tkinter as tk
from PIL import ImageTk, ImageOps, Image

from DTools.fillers import NoFiller


class SketchImage:
    def __init__(self, sketch, path, position, size, filler=None, rotate=0, mirror=False):
        self.sketch = sketch
        self.position = position
        self.size = size
        if filler is None:
            self.filler = NoFiller()
        else:
            self.filler = filler
        self.rotate = rotate
        self.mirror = mirror
        self.raw_image = Image.open(path)
        self.image = None
        self.photo_image = None
        self.id = None

    def update(self, position=None, size=None, filler=None, rotate=None, mirror=None):
        if position is not None:
            self.position = position
        if size is not None:
            self.size = size
        if filler is not None:
            self.filler = filler
        if rotate is not None:
            self.rotate = rotate
        if mirror is not None:
            self.mirror = mirror

        if self.id is not None:
            self.sketch.raw_delete(self.id)
        if not self.have_size():
            return
        self.image = self.raw_image.resize(self.size, Image.NEAREST)
        self.image = self.filler.fill_image(self.image)
        self.image = self.image.rotate(self.rotate, expand=True)

        if self.mirror:
            self.image = ImageOps.mirror(self.image)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.id = self.sketch.create_image(*self.position, image=self.photo_image)

    def set_position(self, x, y):
        self.position = (x, y)
        self.sketch.set_coords(self.id, *self.position)

    def hide(self):
        self.sketch.item_configure(self.id, state=tk.HIDDEN)

    def show(self):
        self.sketch.item_configure(self.id, state=tk.NORMAL)

    def cover_position(self, x, y):
        x2, y2 = self.position
        width, height = self.size
        width_half = width / 2
        height_half = height / 2
        return (x2 - width_half <= x <= x2 + width_half) and (y2 - height_half <= y <= y2 + height_half)

    def have_size(self):
        return all([el>0 for el in self.size])