import inspect


class MarkCommand:
    name = 'mark'

    def __init__(self, sketch, index=None, x=0, y=0):
        _, _, _, self.kwargs = inspect.getargvalues(inspect.currentframe())

        self.kwargs.pop('self')
        self.kwargs.pop('sketch')

        self.name = MarkCommand.name
        self.sketch = sketch

        if self.kwargs['index'] is None:
            self.sketch.mark_object(x, y)
            self.kwargs['index'] = self.sketch.marked_object_index

    def get_kwargs(self):
        return self.kwargs

    def on_move(self, x, y):
        pass

    def on_release(self, x, y):
        self.sketch.add_command(self)

    def do(self):
        if self.kwargs['index'] is None:
            self.sketch.mark_object(self.kwargs['index'],self.kwargs['index'])
        else:
            self.sketch.marked_object_index = self.kwargs['index']
