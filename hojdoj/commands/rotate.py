import numpy as np

from DTools.base_command import BaseCommand


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.mark_object()
        if self.index is None:
            return
        self.orig = self.logic.object_position(self.index)
        self.start_angle = self.get_angle(self.init_event.x, self.init_event.y)

    def on_move(self, event):
        if self.index is None:
            return
        rotation = self.get_angle(event.x,event.y)-self.start_angle
        self.logic.rotate_object(rotation, index=self.index, intermediate=True)

    def on_release(self, event):
        if self.index is None:
            return
        rotation = self.get_angle(event.x,event.y)-self.start_angle
        self.perform_command(self.name,
                             rotation,
                             index=self.index)

    def get_angle(self, x, y):
        x_orig, y_orig = self.orig
        dx = x-x_orig
        dy = y-y_orig
        return np.arctan2(dx, dy)*180/np.pi
