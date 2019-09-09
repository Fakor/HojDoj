import numpy as np


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
        rng = np.hypot(*dpos)
        velocity = tuple(dpos*5/rng)

        self.sketch.new_command(self.name,
                                velocity,
                                index=self.index,
                                range=rng)