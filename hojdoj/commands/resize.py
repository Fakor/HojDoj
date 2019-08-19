from DTools.tools import sum_points


class Command:
    name = 'resize'

    def __init__(self, sketch, index=None, size=(0,0), event=None):
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
            self.org_size = self.image.size
        self.size = size

    def get_kwargs(self):
        return {
            'index': self.index,
            'size': self.size
        }

    def on_move(self, event):
        self._prepare_shape(event.x, event.y)
        self._update_image()

    def on_release(self, event):
        self._prepare_shape(event.x, event.y)
        self.sketch.add_command(self)

    def do(self):
        self._update_image()

    def undo(self):
        self.image.update(size=self.org_size)

    def _prepare_shape(self, x, y):
        dpos = (x - self.mark_x, y - self.mark_y)
        self.size = sum_points(self.org_size, dpos)

    def _update_image(self):
        self.image.update(size=self.size)