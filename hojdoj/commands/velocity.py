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
        dpos = np.array((event.x - self.init_event.x, event.y - self.init_event.y))
        rng = np.hypot(*dpos)
        velocity = tuple(dpos*15/rng)

        self.sketch.new_command(self.name,
                                velocity,
                                index=self.index,
                                range=rng)