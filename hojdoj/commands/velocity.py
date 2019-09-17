import numpy as np

from DTools.base_command import BaseCommand


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.mark_object()

    def on_move(self, event):
        pass

    def on_release(self, event):
        if self.index is None:
            return
        dpos = np.array(self.delta_position(event))
        velocity = tuple(dpos/25)
        kwargs = {'index': self.index}
        if self.button2:
            kwargs['range'] = np.hypot(*dpos)
        self.sketch.new_command(self.name,
                                velocity,
                                **kwargs)
