import inspect


class Command:
    name = 'move'

    def __init__(self, sketch, index=None, dx=0, dy=0, x=0, y=0):
        _,_,_,self.kwargs = inspect.getargvalues(inspect.currentframe())

        self.kwargs.pop('self')
        self.kwargs.pop('sketch')
        self.kwargs.pop('x')
        self.kwargs.pop('y')

        self.name = Command.name
        self.sketch = sketch

        if self.kwargs['index'] is None:
            self.sketch.mark_object(x, y)
            self.kwargs['index'] = self.sketch.marked_object_index
        if self.kwargs['index'] is not None:
            self.start_x, self.start_y = self.sketch.get_coords(self.kwargs['index'])
            self.mark_x = x
            self.mark_y = y

    def get_kwargs(self):
        return self.kwargs

    def on_move(self, x, y):
        if self.kwargs['index'] is None:
            return
        self.kwargs['dx'] = x - self.mark_x
        self.kwargs['dy'] = y - self.mark_y
        self.sketch.set_coords(self.kwargs['index'], self.start_x+self.kwargs['dx'], self.start_y+self.kwargs['dy'])

    def on_release(self, x, y):
        if self.kwargs['index'] is None:
            return
        self.kwargs['dx'] = x - self.mark_x
        self.kwargs['dy'] = y - self.mark_y
        self.sketch.add_command(self)

    def do(self):
        if self.kwargs['index'] is None:
            return
        self.sketch.set_coords(self.kwargs['index'], self.start_x + self.kwargs['dx'], self.start_y + self.kwargs['dy'])

    def undo(self):
        if self.kwargs['index'] is None:
            return
        self.sketch.set_coords(self.kwargs['index'], self.start_x, self.start_y)