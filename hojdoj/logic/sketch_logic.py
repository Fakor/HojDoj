from collections import OrderedDict
from logic.image_logic import ImageLogic
from DTools.fillers import *


class SketchLogic:
    def __init__(self, image_templates, fillers=None):
        self.image_templates = image_templates
        if fillers is None:
            self.fillers = dict()
        else:
            self.fillers = fillers
        self.objects = OrderedDict()
        self.marked_object_index = None
        self.object_index = 0
        self.used_object_indexes = set()

    def step(self):
        ret = []
        for index, obj in self.objects.items():
            if obj.motion_update():
                ret.append((index, obj.position))
        return ret

    def get_object(self, index):
        return self.objects[index]

    def next_image_index(self):
        while self.object_index in self.used_object_indexes:
            self.object_index = self.object_index + 1
        self.used_object_indexes.add(self.object_index)
        return self.object_index

    def object_position(self, index):
        return self.objects[index].position

    def object_velocity(self, index):
        return self.objects[index].velocity

    def object_size(self, index):
        return self.objects[index].size

    def object_rotation(self, index):
        return self.objects[index].rotation

    def get_filler(self, arg):
        if (isinstance(arg, tuple) or isinstance(arg, list)) and len(arg) == 3:
            return ColorFiller(arg)
        elif isinstance(arg, str):
            filler_meta = self.fillers[arg]
            vertical = filler_meta['type'] == 'elastic_vertical'
            return ElasticImageFiller(filler_meta['path'], vertical)
        else:
            return NoFiller()

    def draw_object(self,
                    callback,
                    name,
                    position,
                    size,
                    index=None,
                    rotation=0,
                    mirror=False,
                    filler=None):
        if index is None:
            index = self.next_image_index()
        self.objects[index] = ImageLogic(self.image_templates[name],
                                         position,
                                         size,
                                         rotation=rotation,
                                         mirror=mirror,
                                         filler=self.get_filler(filler))
        self.marked_object_index = index
        return callback(index, position, self.objects[index])

    def delete_object(self, callback, index=None):
        if index is None:
            index = self.marked_object_index
        self.objects.pop(index)
        return callback(index)

    def move_object(self, callback, delta_position, index=None, intermediate=False):
        if index is None:
            index = self.marked_object_index
        position = self.objects[index].move(delta_position, intermediate)
        return callback(index, position)

    def rotate_object(self, callback, rotation, index=None, intermediate=False):
        if index is None:
            index = self.marked_object_index
        self.objects[index].rotate(rotation, intermediate)
        return callback(index, rotation, self.objects[index])

    def resize_object(self, callback, dsize, index=None, intermediate=False):
        if index is None:
            index = self.marked_object_index
        actual_dsize = self.objects[index].resize(dsize, intermediate)
        return callback(index, actual_dsize, self.objects[index])

    def mark_object_by_index(self, callback, index):
        self.marked_object_index = index
        return callback(self.marked_object_index)

    def mark_object(self, callback, position):
        self.marked_object_index = None
        for index, obj in reversed(self.objects.items()):
            if obj.cover_position(*position):
                self.marked_object_index = index
                break
        return callback(self.marked_object_index)

    def set_velocity(self, callback, velocity, index=None, range=None):
        if index is None:
            index = self.marked_object_index
        vel = self.objects[index].set_velocity(velocity, range)
        return callback(index, vel)

    def set_acceleration(self, callback, acceleration, index=None):
        if index is None:
            index = self.marked_object_index
        acc = self.objects[index].set_acceleration(acceleration)
        return callback(index, acc)
