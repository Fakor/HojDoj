import numpy as np

from DTools.base_command import BaseCommand
from DTools.tools import count_jump_range


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
        velocity = tuple(dpos/20)
        acceleration = (0, -2*np.sign(velocity[1]))
        rng = count_jump_range(velocity, acceleration)

        self.sketch.new_command('motion',
                                velocity=velocity,
                                acceleration=acceleration,
                                range=rng)
