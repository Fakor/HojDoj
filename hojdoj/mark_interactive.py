

class MarkInteractive:
    def __init__(self, sketch, event):
        sketch.mark_command(event.x, event.y)

    def on_move(self, event):
        pass

    def on_release(self, event):
        pass