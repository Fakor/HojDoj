import inspect
import tkinter as tk


class Command:
    name = 'delete'

    def __init__(self, sketch, index=None, x=0, y=0):
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
            self.image=self.sketch.objects[self.kwargs['index']]

    def get_kwargs(self):
        return self.kwargs

    def on_move(self, x, y):
        pass

    def on_release(self, x, y):
        if self.kwargs['index'] is None:
            return
        self.sketch.add_command(self)

    def do(self):
        if self.kwargs['index'] is None:
            return
        self.image.hide()

    def undo(self):
        if self.kwargs['index'] is None:
            return
        self.image.show()
