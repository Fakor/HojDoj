from DTools.tools import sum_points


class Command:
    name = 'resize'

    def __init__(self, sketch, event, command_name):
        self.name = command_name
        self.sketch = sketch

        self.index = self.sketch.mark_object((event.x, event.y))
        if self.index is None:
            return
        self.mark_x = event.x
        self.mark_y = event.y

        self.org_size = self.sketch.get_object_size(self.index)

    def on_move(self, event):
        if self.index is None:
            return
        dpos = self.get_dpos(event.x, event.y)
        self.sketch.resize_object(self.index, dpos, intermediate=True)

    def on_release(self, event):
        if self.index is None:
            return
        dpos = self.get_dpos(event.x, event.y)
        self.sketch.new_command(self.name,
                                self.index,
                                dpos)

    def get_dpos(self, x, y):
        return 2*(self.mark_x - x), 2*(self.mark_y - y)
