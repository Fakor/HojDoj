class Command:
    name = 'mark'

    def __init__(self, sketch, event, command_name):
        self.name = command_name
        self.sketch = sketch

        self.index = self.sketch.mark_object((event.x, event.y))

    def on_move(self, event):
        pass

    def on_release(self, event):
        if self.index is not None:
            self.sketch.new_command(self.name,
                                    self.index)
