class Command:
    name='jump'

    def __init__(self, sketch, index=None, dpos=(4, 12), gravity=0.3, step_time=10, event=None):
        self.name = Command.name
        self.sketch = sketch

        if event is not None:
            self.index = self.sketch.mark_object(event.x, event.y)
        else:
            self.index = index
        if self.index is None:
            return
        self.image = self.sketch.objects[self.index]
        self.start_position = self.image.position
        if event and (event.x > self.start_position[0]):
            self.dpos = (-dpos[0], dpos[1])
        else:
            self.dpos = (dpos[0], dpos[1])
        self.gravity = gravity
        self.step_time = step_time

    def get_kwargs(self):
        return {
            'index': self.index,
            'dpos': self.dpos,
            'gravity': self.gravity,
            'step_time': self.step_time
        }

    def on_move(self, event):
        pass

    def on_release(self, event):
        if self.index is None:
            return
        self.sketch.add_command(self)

    def do(self):
        self._update_image(self.dpos)

    def undo(self):
        if self.index is None:
            return
        self.image.update(position=self.start_position)

    def _update_image(self, dpos):
        new_x = self.image.position[0] + dpos[0]
        new_y = self.image.position[1] - dpos[1]

        if new_y > self.start_position[1]:
            new_y = self.start_position[1]
            self.image.update(position=(int(new_x), int(new_y)))
        else:
            self.image.update(position=(int(new_x), int(new_y)))
            dy = dpos[1] - self.gravity
            self.sketch.after(self.step_time, self._update_image, (dpos[0], dy))
