from collections import OrderedDict


class SketchLogic:
    def __init__(self):
        self.objects = OrderedDict()
        self.marked_object_index = None

    def add_object(self, index, new_object):
        self.objects[index] = new_object

    def delete(self, index):
        self.objects.pop(index)

    def mark_object(self, x, y):
        for index, obj in reversed(self.objects.items()):
            if obj.cover_position(x,y):
                self.marked_object_index = index
                return self.marked_object_index
        self.marked_object_index = None
        return None