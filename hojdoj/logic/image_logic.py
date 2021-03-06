from PIL import Image, ImageOps
import numpy as np

from DTools.fillers import NoFiller
from DTools.tools import sum_points


class ImageLogic:
    # This constant is added to make gravity more stable.
    # If set to 0 there is a high chance that the force
    # applied will throw the object out of the screen in
    # a non-entertaining way.
    GRAVITY_MIN_RANGE = 20

    def __init__(self,
                 path,
                 position,
                 size,
                 filler=None,
                 rotation=0,
                 mirror=False,
                 velocity=(0, 0),
                 acceleration=(0, 0),
                 mass=None):
        self.position = position
        self.size = size
        if filler is None:
            self.filler = NoFiller()
        else:
            self.filler = filler
        self.rotation = rotation
        self.mirror = mirror
        self.velocity = velocity
        self._acceleration = acceleration
        self.gravity_acceleration = (0, 0)
        self.range = None
        if mass is None:
            self.mass = np.prod(self.size)
        else:
            self.mass = mass
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
        self.velocity = velocity
        self.range = range
        return velocity

    def set_acceleration(self, acceleration):
        self._acceleration = acceleration
        return acceleration

    def set_motion(self, velocity=None, acceleration=None, range=None):
        if velocity is not None:
            self.velocity = velocity
        if acceleration is not None:
            self._acceleration = acceleration
        if range is not None:
            self.range = range

    @property
    def acceleration(self):
        return sum_points(self._acceleration, self.gravity_acceleration)

    def apply_gravity(self, obj, gravity):
        dist = np.array(obj.position) - np.array(self.position)
        r = np.max((np.linalg.norm(dist), ImageLogic.GRAVITY_MIN_RANGE))
        acc = gravity*obj.mass/r**2
        added_acc = tuple(acc * el/r for el in dist)
        self.gravity_acceleration = sum_points(self.gravity_acceleration, added_acc)

    def reset_gravity_acceleration(self):
        self.gravity_acceleration = (0, 0)

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
        self.velocity = sum_points(self.velocity, self.acceleration)
        if self.range is not None:
            d_range = np.hypot(*self.velocity)
            if d_range > self.range:
                velocity = np.array(self.velocity) * self.range / d_range
                self.velocity = (0, 0)
                self._acceleration = (0, 0)
                self.range = None
            else:
                velocity = self.velocity
                self.range -= d_range
            self.position = sum_points(self.position, velocity)
        else:
            self.position = sum_points(self.position, self.velocity)
        return org_pos != self.position

    def have_size(self):
        return all([el > 0 for el in self.size])
