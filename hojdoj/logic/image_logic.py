from PIL import Image, ImageOps
import numpy as np

from DTools.fillers import NoFiller
from DTools.tools import sum_points


class ImageLogic:
    def __init__(self, path, position, size, filler=None, rotation=0, mirror=False, velocity=(0,0)):
        self.position = position
        self.size = size
        if filler is None:
            self.filler = NoFiller()
        else:
            self.filler = filler
        self.rotation = rotation
        self.mirror = mirror
        self.velocity = np.array(velocity)
        self.range = None
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
        new_pos = sum_points(self.position, delta_position)
        if not intermediate:
            self.position = new_pos
        return new_pos

    def rotate(self, rotation, intermediate=False):
        new_rotation = np.mod(self.rotation+rotation, 360)
        self.update(rotation=new_rotation)
        if intermediate:
            self.rotation = self.rotation-rotation
        return new_rotation

    def resize(self, dsize, intermediate=False):
        old_size = self.size
        new_size = sum_points(self.size, dsize, min_value=0)
        self.update(size=new_size)
        if intermediate:
            self.size = old_size
        return new_size

    def set_velocity(self, velocity, range=None):
        self.velocity = np.array(velocity)
        self.range = range
        return velocity

    def update(self, position=None, size=None, filler=None, rotation=None, mirror=None):
        if position is not None:
            self.position = position
        if size is not None:
            self.size = size
        if filler is not None:
            self.filler = filler
        if rotation is not None:
            self.rotation = rotation
        if mirror is not None:
            self.mirror = mirror

        if not self.have_size():
            return
        self.image = self.raw_image.resize(self.size, Image.NEAREST)
        self.image = self.filler.fill_image(self.image)
        self.image = self.image.rotate(self.rotation, expand=True)

        if self.mirror:
            self.image = ImageOps.mirror(self.image)

    def motion_update(self):
        org_pos = self.position
        if self.range is not None:
            d_range = np.sqrt(np.sum(self.velocity ** 2))
            if d_range > self.range:
                velocity = self.velocity * self.range / d_range
                self.velocity = np.array((0, 0))
                self.range = 0
            else:
                velocity = self.velocity
                self.range -= d_range
            self.position = sum_points(self.position, velocity)
        else:
            self.position = sum_points(self.position, self.velocity)
        return org_pos != self.position

    def have_size(self):
        return all([el > 0 for el in self.size])