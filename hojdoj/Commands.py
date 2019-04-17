from PIL import Image, ImageTk

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
        self.start_x = event.x
        self.start_y = event.y
        self.path = self.sketch.current_image
        self.id = None

    def on_move(self, event):
        self._prepare_shape(event)

        if self.id is not None:
            self.sketch.delete(self.id)
        if self.width == 0 or self.height == 0:
            return
        self.image = Image.open(self.path)
        self.image = self.image.resize((self.width, self.height), Image.ANTIALIAS)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.id = self.sketch.create_image(self.x, self.y, image=self.photo_image)

    def on_release(self, event):
        if self.id is not None:
            self.sketch.delete(self.id)
            self.sketch.sketch_image(self.x, self.y, self.width, self.height, self.path)

    def _prepare_shape(self, event):
        self.width = abs(event.x - self.start_x)
        self.height = abs(event.y - self.start_y)

        self.x = (event.x + self.start_x) / 2
        self.y = (event.y + self.start_y) / 2
