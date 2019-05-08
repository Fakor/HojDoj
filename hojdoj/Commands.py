from PIL import Image, ImageTk, ImageOps

from tools import elastic_background


class SketchRectInteractive:

    def __init__(self, sketch, event):
        self.sketch = sketch
        self.start_point = (event.x, event.y)

    def on_move(self, event):
        self.sketch.filler.update(self.start_point, event)

    def on_release(self, event):
        self.sketch.filler.make_sketch(self.start_point, event)


class SketchImageInteractive:
    def __init__(self, sketch, event):
        self.sketch = sketch
        self.start_x = event.x
        self.start_y = event.y
        self.path = self.sketch.current_image
        self.org_image = self.sketch.filler.fill_image(self.path)
        self.image = None
        self.id = None

    def on_move(self, event):
        self._prepare_shape(event)

        if self.id is not None:
            self.sketch.delete(self.id)
        if self.width == 0 or self.height == 0:
            return

        self.image = self.org_image.resize((self.width, self.height), Image.ANTIALIAS)
        self.image = self.image.rotate(self.rotate)
        if self.mirror:
            self.image = ImageOps.mirror(self.image)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.id = self.sketch.create_image(self.x, self.y, image=self.photo_image)

    def on_release(self, event):
        if self.width == 0 or self.height == 0:
            return
        if self.id is not None:
            self.sketch.delete(self.id)
            self.sketch.sketch_image(self.x, self.y, self.width, self.height,
                                     self.path, self.sketch.filler.color['RGB'], rotate=self.rotate, mirror=self.mirror)

    def _prepare_shape(self, event):
        self.width = abs(event.x - self.start_x)
        self.height = abs(event.y - self.start_y)

        if event.y < self.start_y:
            self.rotate = 180
            if event.x > self.start_x:
                self.mirror = True
            else:
                self.mirror = False
        else:
            self.rotate = 0
            if event.x < self.start_x:
                self.mirror = True
            else:
                self.mirror = False

        self.x = int((event.x + self.start_x) / 2)
        self.y = int((event.y + self.start_y) / 2)


class SketchElasticImageInteractive:
    def __init__(self, sketch, event):
        self.sketch = sketch
        self.start_x = event.x
        self.start_y = event.y
        self.path = self.sketch.elastic_image
        self.image = None
        self.id = None

    def on_move(self, event):
        self._prepare_shape(event)
        if self.id is not None:
            self.sketch.delete(self.id)
        if self.width == 0 or self.height == 0:
            return

        self.image = elastic_background(self.path, (self.width, self.height))
        self.id = self.sketch.create_image(self.x, self.y, image=self.image)

    def on_release(self, event):
        print(self.width, self.height, self.x, self.y)
        self._prepare_shape(event)
        if self.width == 0 or self.height == 0:
            return
        if self.id is not None:
            self.sketch.delete(self.id)
            self.sketch.sketch_elastic_image(self.x, self.y, self.width, self.height, self.path)

    def _prepare_shape(self, event):
        self.width = abs(event.x - self.start_x)
        self.height = abs(event.y - self.start_y)

        self.x = int((event.x + self.start_x) / 2)
        self.y = int((event.y + self.start_y) / 2)