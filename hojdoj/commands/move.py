from DTools.tools import sum_points


class Command:
    name = 'move'

    def __init__(self, sketch, event, command_name):
        self.name = Command.name
        self.sketch = sketch

        if event is not None:
            self.index = self.sketch.mark_object(event.x, event.y)
            self.mark_x = event.x
            self.mark_y = event.y
        else:
            self.index = index

        if self.index is not None:
            self.image = self.sketch.objects[self.index]
            self.start_pos = self.image.position
            self.dpos = dpos

    def get_kwargs(self):
        return {
            'index': self.index,
            'dpos': self.dpos
        }

    def on_move(self, event):
        if self.index is None:
            return
        self.dpos = (event.x - self.mark_x, event.y - self.mark_y)
        self.image.set_position(*sum_points(self.start_pos, self.dpos))

    def on_release(self, event):
        if self.index is None:
            return
        self.dpos = (event.x - self.mark_x, event.y - self.mark_y)
        self.sketch.add_command(self)

    def do(self):
        if self.index is None:
            return
        self.image.set_position(*sum_points(self.start_pos, self.dpos))

    def undo(self):
        if self.index is None:
            return
        self.image.set_position(*self.start_pos)