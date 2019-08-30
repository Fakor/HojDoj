from PIL import Image, ImageOps

from DTools.fillers import NoFiller
from DTools.tools import sum_points


class ImageLogic:
    def __init__(self, path, position, size, filler=None, rotate=0, mirror=False):
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
        self.update()

    def cover_position(self, x,y ):
        x2, y2 = self.position
        width, height = self.size
        width_half = width / 2
        height_half = height / 2
        return (x2 - width_half <= x <= x2 + width_half) and (y2 - height_half <= y <= y2 + height_half)

    def move(self, delta_position, intermediate=False):
        new_pos = tuple(sum_points(self.position, delta_position))
        if not intermediate:
            self.position = new_pos
        return new_pos

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

        if not self.have_size():
            return
        self.image = self.raw_image.resize(self.size, Image.NEAREST)
        self.image = self.filler.fill_image(self.image)
        self.image = self.image.rotate(self.rotate, expand=True)

        if self.mirror:
            self.image = ImageOps.mirror(self.image)

    def have_size(self):
        return all([el > 0 for el in self.size])