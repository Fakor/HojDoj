class Command:
    def __init__(self, sketch, event, command_name):
        self.name = command_name
        self.sketch = sketch

        self.index = self.sketch.mark_object((event.x, event.y))
        if self.index is None:
            return
        self.mark_x = event.x
        self.mark_y = event.y
        pos = self.sketch.get_object_position(self.index)
        self.mark_on_right = pos[0] < self.mark_x
        self.mark_on_up = pos[1] < self.mark_y

    def on_move(self, event):
        if self.index is None:
            return
        dpos = self.get_dpos(event.x, event.y)
        self.sketch.resize_object(dpos, index=self.index, intermediate=True)

    def on_release(self, event):
        if self.index is None:
            return
        dpos = self.get_dpos(event.x, event.y)
        self.sketch.new_command(self.name,
                                dpos,
                                index=self.index)

    def get_dpos(self, x, y):
        dx = 2*(self.mark_x - x)
        if self.mark_on_right:
            dx *= -1
        dy = 2 * (self.mark_y - y)
        if self.mark_on_up:
            dy *= -1
        return dx, dy
