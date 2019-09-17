import numpy as np

from DTools.base_command import BaseCommand

MAX_RANGE = 2000
MAX_ACC = 1


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
        rng = np.hypot(*dpos)
        scale = np.min((rng/MAX_RANGE, 1))
        acceleration = tuple(dpos*scale/rng)

        self.sketch.new_command(self.name,
                                acceleration,
                                index=self.index)