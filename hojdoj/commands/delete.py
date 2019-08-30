class Command:
    name = 'delete'

    def __init__(self, sketch, event, command_name):
        self.command_name = command_name
        self.sketch = sketch
        self.index = self.sketch.mark_object((event.x, event.y))

    def on_move(self, event):
        pass

    def on_release(self, event):
        if self.index is None:
            return
        self.sketch.new_command(self.command_name,
                                self.index)
