import numpy as np


class Command:
    name = 'rotate'

    def __init__(self, sketch, index=None, degrees=0, event=None):
        self.name = Command.name
        self.sketch = sketch

        if event is not None:
            self.index = self.sketch.mark_object(event.x, event.y)
        else:
            self.index = index
        if self.index is not None:
            self.image = self.sketch.objects[self.index]
            self.image_angle = self.image.rotate
            if event:
                self.start_angle = self.get_angle(event.x, event.y)
        self.degrees = degrees

    def get_kwargs(self):
        return {
            'index': self.index,
            'degrees': self.degrees
        }

    def on_move(self, event):
        if self.index is None:
            return
        self.degrees = self.get_angle(event.x,event.y)-self.start_angle
        self._update_image()

    def on_release(self, event):
        if self.index is None:
            return
        self.degrees = self.get_angle(event.x,event.y)-self.start_angle
        self.sketch.add_command(self)

    def do(self):
        self._update_image()

    def undo(self):
        self.image.update(rotate=self.image_angle)

    def _update_image(self):
        self.image.update(rotate=self.image_angle+self.degrees)

    def get_angle(self, x, y):
        x_orig, y_orig = self.image.position
        dx = x-x_orig
        dy = y-y_orig
        return np.arctan2(dx, dy)*180/np.pi
