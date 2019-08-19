class Command:
    name = 'mark'

    def __init__(self, sketch, index=None, event=None):
        self.name = Command.name
        self.sketch = sketch

        self.orig_marked = self.sketch.marked_object_index

        if event is not None:
            self.index = self.sketch.mark_object(event.x, event.y)
        else:
            self.index = index

    def get_kwargs(self):
        return {
            'index': self.index
        }

    def on_move(self, event):
        pass

    def on_release(self, event):
        if self.index is not None:
            self.sketch.add_command(self)

    def do(self):
        if self.index is not None:
            self.sketch.marked_object_index = self.index

    def undo(self):
        self.sketch.marked_object_index = self.orig_marked
