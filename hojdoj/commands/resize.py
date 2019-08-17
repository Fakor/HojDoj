import inspect


class Command:
    name = 'resize'

    def __init__(self, sketch, index=None, width=0, height=0, event=None):
        _,_,_,self.kwargs = inspect.getargvalues(inspect.currentframe())

        self.kwargs.pop('self')
        self.kwargs.pop('sketch')
        self.kwargs.pop('event')

        self.name = Command.name
        self.sketch = sketch

        if self.kwargs['index'] is None:
            self.sketch.mark_object(event.x, event.y)
            self.kwargs['index'] = self.sketch.marked_object_index
        if self.kwargs['index'] is not None:
            self.image = self.sketch.objects[self.kwargs['index']]
            self.org_size = self.image.size
        if event:
            self.mark_x = event.x
            self.mark_y = event.y

    def get_kwargs(self):
        return self.kwargs

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
        dx = x - self.mark_x
        dy = y - self.mark_y
        self.kwargs['width'] = self.org_size[0] + dx
        self.kwargs['height'] = self.org_size[1] + dy

    def _get_image_position(self):
        return self.org_position

    def _get_image_size(self):
        return self.kwargs['width'], self.kwargs['height']

    def _update_image(self):
        self.image.update(size=self._get_image_size())