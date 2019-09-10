import numpy as np

from DTools.tools import count_jump_range


class Command:
    def __init__(self, sketch, event, command_name):
        self.name = command_name
        self.sketch = sketch

        self.index = self.sketch.mark_object((event.x, event.y))
        if self.index is None:
            return
        self.mark_x = event.x
        self.mark_y = event.y

    def on_move(self, event):
        pass

    def on_release(self, event):
        if self.index is None:
            return
        dpos = np.array((event.x - self.mark_x, event.y - self.mark_y))
        velocity = tuple(dpos/20)
        acceleration = (0, -2*np.sign(velocity[1]))
        rng = count_jump_range(velocity, acceleration)

        self.sketch.new_command('motion',
                                velocity=velocity,
                                acceleration=acceleration,
                                range=rng)
