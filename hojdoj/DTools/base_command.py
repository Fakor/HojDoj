class BaseCommand:
    def __init__(self, sketch, event, command_name, button2=False):
        self.name = command_name
        self.sketch = sketch
        self.init_event = event
        self.button2 = button2
        self.index = None

    def on_move(self, event):
        raise NotImplemented

    def on_release(self, event):
        raise NotImplemented

    def mark_object(self):
        self.index = self.sketch.mark_object((self.init_event.x, self.init_event.y))
        return self.index is not None
