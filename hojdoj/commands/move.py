class Command:
    name = 'move'

    def __init__(self, sketch, event, command_name):
        self.name = command_name
        self.sketch = sketch

        self.index = self.sketch.mark_object((event.x, event.y))
        if self.index is None:
            return
        self.mark_x = event.x
        self.mark_y = event.y
        self.dpos = (0,0)

    def on_move(self, event):
        if self.index is None:
            return
        self.dpos = (event.x - self.mark_x, event.y - self.mark_y)
        self.sketch.move_object(self.index, self.dpos, intermediate=True)

    def on_release(self, event):
        if self.index is None:
            return
        self.dpos = (event.x - self.mark_x, event.y - self.mark_y)
        self.sketch.new_command(self.name,
                                self.index,
                                self.dpos)
