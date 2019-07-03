

class MoveInteractive:
    def __init__(self, sketch, event):
        self.sketch = sketch
        self.start_x = event.x
        self.start_y = event.y
        self.sketch.mark_object(self.start_x, self.start_y)
        self.index = self.sketch.marked_object_index

    def on_move(self, event):
        pass

    def on_release(self, event):
        self.sketch.move_command(self.index, event.x-self.start_x, event.y-self.start_y)
