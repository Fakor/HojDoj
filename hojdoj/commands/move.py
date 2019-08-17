import inspect


class Command:
    name = 'move'

    def __init__(self, sketch, index=None, dx=0, dy=0, event=None):
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
            self.start_x, self.start_y = self.image.position
            self.mark_x = event.x
            self.mark_y = event.y

    def get_kwargs(self):
        return self.kwargs

    def on_move(self, event):
        if self.kwargs['index'] is None:
            return
        self.kwargs['dx'] = event.x - self.mark_x
        self.kwargs['dy'] = event.y - self.mark_y
        self.image.set_position(self.start_x+self.kwargs['dx'], self.start_y+self.kwargs['dy'])

    def on_release(self, event):
        if self.kwargs['index'] is None:
            return
        self.kwargs['dx'] = event.x - self.mark_x
        self.kwargs['dy'] = event.y - self.mark_y
        self.sketch.add_command(self)

    def do(self):
        if self.kwargs['index'] is None:
            return
        self.image.set_position(self.start_x + self.kwargs['dx'], self.start_y + self.kwargs['dy'])

    def undo(self):
        if self.kwargs['index'] is None:
            return
        self.image.set_position(self.start_x, self.start_y)