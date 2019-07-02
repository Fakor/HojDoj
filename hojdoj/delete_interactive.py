

class DeleteInteractive:
    def __init__(self, sketch, event):
        self.sketch = sketch

    def on_move(self, event):
        print('Move', event.x, event.y)

    def on_release(self, event):
        print('Release', event.widget)
