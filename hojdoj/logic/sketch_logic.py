from collections import OrderedDict
from logic.image_logic import ImageLogic


class SketchLogic:
    def __init__(self, image_templates):
        self.image_templates = image_templates
        self.objects = OrderedDict()
        self.marked_object_index = None
        self.object_index = 0
        self.used_object_indexes = set()

    def get_object(self, index):
        return self.objects[index]

    def get_command_table(self):
        return {
            'draw': self.draw_object,
            'move': self.move_object
        }

    def next_image_index(self):
        while self.object_index in self.used_object_indexes:
            self.object_index = self.object_index + 1
        self.used_object_indexes.add(self.object_index)
        return self.object_index

    def object_position(self, index):
        return self.objects[index].position

    def object_size(self, index):
        return self.objects[index].size

    def draw_object(self, callback, name, position, size, index=None):
        if index is None:
            index = self.next_image_index()
        self.objects[index] = ImageLogic(self.image_templates[name], position, size)
        return callback(index, position, self.objects[index])

    def delete_object(self, index):
        self.objects.pop(index)

    def move_object(self, callback, index, delta_position, intermediate=False):
        position = self.objects[index].move(delta_position, intermediate)
        return callback(index, position)

    def mark_object(self, callback, position):
        self.marked_object_index = None
        for index, obj in reversed(self.objects.items()):
            if obj.cover_position(*position):
                self.marked_object_index = index
                break
        return callback(self.marked_object_index)
