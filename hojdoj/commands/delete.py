class Command:
    name = 'delete'

    def __init__(self, sketch, index=None, event=None):
        self.name = Command.name
        self.sketch = sketch

        if event is not None:
            self.index = self.sketch.mark_object(event.x, event.y)
        else:
            self.index = index
        if self.index is not None:
            self.image=self.sketch.objects[self.index]

    def get_kwargs(self):
        return {
            'index': self.index
        }

    def on_move(self, event):
        pass

    def on_release(self, event):
        if self.index is None:
            return
        self.sketch.add_command(self)

    def do(self):
        if self.index is None:
            return
        self.image.hide()

    def undo(self):
        if self.index is None:
            return
        self.image.show()
