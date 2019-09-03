from collections import OrderedDict
from logic.image_logic import ImageLogic
from DTools.fillers import *


class SketchLogic:
    def __init__(self, image_templates):
        self.image_templates = image_templates
        self.objects = OrderedDict()
        self.marked_object_index = None
        self.object_index = 0
        self.used_object_indexes = set()

    def get_object(self, index):
        return self.objects[index]

    def next_image_index(self):
        while self.object_index in self.used_object_indexes:
            self.object_index = self.object_index + 1
        self.used_object_indexes.add(self.object_index)
        return self.object_index

    def object_position(self, index):
        return self.objects[index].position

    def object_size(self, index):
        return self.objects[index].size

    def object_rotation(self, index):
        return self.objects[index].rotation

    def get_filler(self, arg):
        if (isinstance(arg, tuple) or isinstance(arg, list)) and len(arg) == 3:
            return ColorFiller(arg)
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

    def rotate_object(self, callback, index, rotation, intermediate=False):
        self.objects[index].rotate(rotation, intermediate)
        return callback(index, rotation, self.objects[index])

    def resize_object(self, callback, index, dsize, intermediate=False):
        actual_dsize = self.objects[index].resize(dsize, intermediate)
        return callback(index, actual_dsize, self.objects[index])

    def mark_object(self, callback, position):
        self.marked_object_index = None
        for index, obj in reversed(self.objects.items()):
            if obj.cover_position(*position):
                self.marked_object_index = index
                break
        return callback(self.marked_object_index)
