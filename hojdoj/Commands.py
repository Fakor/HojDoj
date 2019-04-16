import tkinter as tk


class SketchLineInteractive:

    def __init__(self, sketch, event):
        self.sketch = sketch
        self.start_point = (event.x, event.y)
        self.kwargs = {'fill': self.sketch.fill_color}
        self.id = None

    def on_move(self, event):
        args = (*self.start_point, event.x, event.y)
        if self.id is None:
            self.id = self.sketch.create_line(*args, **self.kwargs)
        else:
            self.sketch.coords(self.id, *args)

    def on_release(self, event):
        if self.id is not None:
            self.sketch.delete(self.id)
            self.sketch.sketch_line(*self.start_point, event.x, event.y, **self.kwargs)


class SketchRectInteractive:

    def __init__(self, sketch, event):
        self.sketch = sketch
        self.start_point = (event.x, event.y)
        self.kwargs = {'fill': self.sketch.fill_color}
        self.id = None

    def on_move(self, event):
        args = (*self.start_point, event.x, event.y)
        if self.id is None:
            self.id = self.sketch.create_rectangle(*args, **self.kwargs)
        else:
            self.sketch.coords(self.id, *args)

    def on_release(self, event):
        if self.id is not None:
            self.sketch.delete(self.id)
            self.sketch.sketch_rect(*self.start_point, event.x, event.y, **self.kwargs)


class SketchImageInteractive:
    def __init__(self, sketch, event):
        self.sketch = sketch
        self.start_point = (event.x, event.y)
        self.id = self.sketch.sketch_image(*self.start_point, self.sketch.current_image)

    def on_move(self, event):
        pass

    def on_release(self, event):
        pass