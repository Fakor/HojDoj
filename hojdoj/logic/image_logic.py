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

    def cover_position(self, x, y):
        x2, y2 = self.position
        width, height = self.size
        width_half = width / 2
        height_half = height / 2
        return (x2 - width_half <= x <= x2 + width_half) and (y2 - height_half <= y <= y2 + height_half)

    def move(self, delta_position):
        self.position = sum_points(self.position, delta_position)