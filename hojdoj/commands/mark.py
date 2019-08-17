import inspect


class Command:
    name = 'mark'

    def __init__(self, sketch, index=None, event=None):
        _, _, _, self.kwargs = inspect.getargvalues(inspect.currentframe())

        self.kwargs.pop('self')
        self.kwargs.pop('sketch')
        self.kwargs.pop('event')

        self.name = Command.name
        self.sketch = sketch

        self.orig_marked = self.sketch.marked_object_index

        if self.kwargs['index'] is None:
            self.sketch.mark_object(event.x, event.y)
            self.kwargs['index'] = self.sketch.marked_object_index

    def get_kwargs(self):
        return self.kwargs

    def on_move(self, event):
        pass

    def on_release(self, event):
        if self.kwargs['index'] is not None:
            self.sketch.add_command(self)

    def do(self):
        if self.kwargs['index'] is not None:
            self.sketch.marked_object_index = self.kwargs['index']

    def undo(self):
        self.sketch.marked_object_index = self.orig_marked
