import inspect


class Command:
    name = 'resize'

    def __init__(self, sketch, index=None, width=0, height=0, x=0, y=0):
        _,_,_,self.kwargs = inspect.getargvalues(inspect.currentframe())

        self.kwargs.pop('self')
        self.kwargs.pop('sketch')

        self.name = Command.name
        self.sketch = sketch

        if self.kwargs['index'] is None:
            self.sketch.mark_object(x, y)
            self.kwargs['index'] = self.sketch.marked_object_index
        if self.kwargs['index'] is not None:
            self.image = self.sketch.objects[self.kwargs['index']]
            self.org_size = self.image.size
            self.mark_x = x
            self.mark_y = y

    def get_kwargs(self):
        return self.kwargs

    def on_move(self, x, y):
        self._prepare_shape(x, y)
        self._update_image()

    def on_release(self, x, y):
        self._prepare_shape(x,y)
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