

class DeleteInteractive:
    def __init__(self, sketch, event):
        self.sketch = sketch
        self.sketch.mark_object(event.x, event.y)
        self.sketch.delete_command(self.sketch.marked_object_index)

    def on_move(self, event):
        pass

    def on_release(self, event):
        pass
