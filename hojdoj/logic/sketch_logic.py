from collections import OrderedDict
from logic.image_logic import ImageLogic
from DTools.fillers import *


class SketchLogic:
    def __init__(self, config, callback):
        self.image_templates = config['image_templates']
        self.fillers = config['fillers']
        self.gravity = config['gravity']
        self.current_image = config['default_image']
        self.current_filler = config['default_color']
        self.callback = callback
        self.objects = OrderedDict()
        self.marked_object_index = None
        self.object_index = 0
        self.used_object_indexes = set()

    def step(self):
        self.apply_gravity_all()
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

    def object_acceleration(self, index):
        return self.objects[index].acceleration

    def object_range(self, index):
        return self.objects[index].range

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

    def get_command_table(self):
        return {
            'draw': self.draw_object,
            'mark': self.mark_object_by_index,
            'delete': self.delete_object,
            'move': self.move_object,
            'rotate': self.rotate_object,
            'resize': self.resize_object
        }

    def draw_object(self,
                    name,
                    position,
                    size,
                    index=None,
                    rotation=0,
                    mirror=False,
                    filler=None,
                    mass=None,
                    velocity=(0, 0),
                    acceleration=(0, 0)):
        if index is None:
            index = self.next_image_index()
        self.objects[index] = ImageLogic(self.image_templates[name],
                                         position,
                                         size,
                                         rotation=rotation,
                                         mirror=mirror,
                                         filler=self.get_filler(filler),
                                         mass=mass,
                                         velocity=velocity,
                                         acceleration=acceleration)
        self.marked_object_index = index
        return self.callback([('draw', {'index': index})])

    def delete_object(self, index=None):
        if index is None:
            index = self.marked_object_index
        self.objects.pop(index)
        return self.callback([('delete', {'index': index})])

    def move_object(self, delta_position, index=None, intermediate=False):
        if index is None:
            index = self.marked_object_index
        position = self.objects[index].move(delta_position, intermediate)
        return self.callback([('move', {'index': index, 'position': position})])

    def rotate_object(self, rotation, index=None, intermediate=False):
        if index is None:
            index = self.marked_object_index
        self.objects[index].rotate(rotation, intermediate)
        return self.callback([('rotate', {'index': index, 'rotation': rotation})])

    def resize_object(self, dsize, index=None, intermediate=False):
        if index is None:
            index = self.marked_object_index
        actual_dsize = self.objects[index].resize(dsize, intermediate)
        return self.callback([('resize', {'index': index, 'size': actual_dsize})])

    def mark_object_by_index(self, index):
        self.marked_object_index = index
        return self.callback([('mark', {'index': self.marked_object_index})])

    def mark_object(self, position):
        self.marked_object_index = None
        actions = []
        for index, obj in reversed(self.objects.items()):
            if obj.cover_position(*position):
                self.marked_object_index = index
                actions.append(('mark', {'index': self.marked_object_index}))
                break
        return self.callback(actions)

    def set_velocity(self, callback, velocity, index=None, range=None):
        if index is None:
            index = self.marked_object_index
        vel = self.objects[index].set_velocity(velocity, range)
        return callback(index, vel)

    def set_motion(self, index=None, **kwargs):
        if index is None:
            index = self.marked_object_index
        self.objects[index].set_motion(**kwargs)

    def set_acceleration(self, callback, acceleration, index=None):
        if index is None:
            index = self.marked_object_index
        acc = self.objects[index].set_acceleration(acceleration)
        return callback(index, acc)

    def apply_gravity_all(self):
        for i1, obj1 in self.objects.items():
            obj1.reset_gravity_acceleration()
            for i2, obj2 in self.objects.items():
                if i1 != i2:
                    obj1.apply_gravity(obj2, self.gravity)
