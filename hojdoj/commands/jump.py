import numpy as np

from DTools.base_command import BaseCommand
from DTools.tools import count_jump_range


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.mark_object()
        if self.button2:
            dx = np.sign(self.logic.object_position(self.index)[0]-self.init_event.x)*5
            velocity = (dx, -20)
            acceleration = (0, 1)
            rng = count_jump_range(velocity, acceleration)
            self.perform_command('motion',
                                 velocity=velocity,
                                 acceleration=acceleration,
                                 range=rng)

    def on_move(self, event):
        pass

    def on_release(self, event):
        if self.index is None or self.button2:
            return
        dpos = np.array(self.delta_position(event))
        velocity = tuple(dpos/20)
        acceleration = (0, -2*np.sign(velocity[1]))
        rng = count_jump_range(velocity, acceleration)

        self.perform_command('motion',
                             velocity=velocity,
                             acceleration=acceleration,
                             range=rng)
