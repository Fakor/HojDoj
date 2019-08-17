import inspect
import numpy as np


class Command:
    name = 'rotate'

    def __init__(self, sketch, index=None, degrees=0, event=None):
        _,_,_,self.kwargs = inspect.getargvalues(inspect.currentframe())

        self.kwargs.pop('self')
        self.kwargs.pop('sketch')
        self.kwargs.pop('event')

        self.name = Command.name
        self.sketch = sketch

        if self.kwargs['index'] is None:
            self.sketch.mark_object(event.x, event.y)
            self.kwargs['index'] = self.sketch.marked_object_index
        if self.kwargs['index'] is not None:
            self.image = self.sketch.objects[self.kwargs['index']]
            self.image_angle = self.image.rotate
        if event:
            self.start_angle = self.get_angle(event.x, event.y)

    def get_kwargs(self):
        return self.kwargs

    def on_move(self, event):
        if self.kwargs['index'] is None:
            return
        self.kwargs['degrees'] = self.get_angle(event.x,event.y)-self.start_angle
        self._update_image()

    def on_release(self, event):
        if self.kwargs['index'] is None:
            return
        self.kwargs['degrees'] = self.get_angle(event.x,event.y)-self.start_angle
        self.sketch.add_command(self)

    def do(self):
        self._update_image()

    def undo(self):
        self.image.update(rotate=self.image_angle)

    def _update_image(self):
        self.image.update(rotate=self.image_angle+self.kwargs['degrees'])

    def get_angle(self, x, y):
        x_orig, y_orig = self.image.position
        dx = x-x_orig
        dy = y-y_orig
        return np.arctan2(dx, dy)*180/np.pi
