import numpy as np


class Command:
    def __init__(self, sketch, event, command_name):
        self.name = command_name
        self.sketch = sketch

        self.index = self.sketch.mark_object((event.x, event.y))
        if self.index is None:
            return
        self.orig = self.sketch.get_object_position(self.index)
        self.start_angle = self.get_angle(event.x, event.y)

    def on_move(self, event):
        if self.index is None:
            return
        rotation = self.get_angle(event.x,event.y)-self.start_angle
        self.sketch.rotate_object(self.index, rotation, intermediate=True)

    def on_release(self, event):
        if self.index is None:
            return
        rotation = self.get_angle(event.x,event.y)-self.start_angle
        self.sketch.new_command(self.name,
                                self.index,
                                rotation)

    def get_angle(self, x, y):
        x_orig, y_orig = self.orig
        dx = x-x_orig
        dy = y-y_orig
        return np.arctan2(dx, dy)*180/np.pi
