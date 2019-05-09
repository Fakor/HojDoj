from PIL import Image

from tools import elastic_background, image_replace_white
from tools import Colors


class ColorFiller:
    def __init__(self, sketch, color):
        self.sketch = sketch
        self.color = color
        self.id = None
        self.image = None

    def update(self, start_point, event):
        args = (*start_point, event.x, event.y)
        if self.id is None:
            self.id = self.sketch.create_rectangle(*args, fill=self.color['tk'])
        else:
            self.sketch.coords(self.id, *args)

    def make_sketch(self, start_point, event):
        if self.id is not None:
            self.sketch.delete(self.id)
            self.sketch.sketch_rect(*start_point, event.x, event.y, fill=self.color['tk'])
        self.id = None

    def fill_image(self, file_path):
        self.image = Image.open(file_path)
        return image_replace_white(self.image, self.color['RGB'])


class ElasticImageFiller:
    def __init__(self, sketch, path):
        self.sketch = sketch
        self.path = path
        self.image = None
        self.id =None
        self.color = Colors.WHITE

    def update(self, start_point, event):
        self._prepare_shape(start_point, event)
        if self.id is not None:
            self.sketch.delete(self.id)
        if self.width == 0 or self.height == 0:
            return
        self.image = elastic_background(self.path, (self.width, self.height))
        self.id = self.sketch.create_image(self.x, self.y, image=self.image)

    def make_sketch(self, start_point, event):
        if self.id is not None:
            self._prepare_shape(start_point, event)
            if self.width == 0 or self.height == 0:
                return
            self.sketch.delete(self.id)
            self.sketch.sketch_elastic_image(self.x, self.y, self.width, self.height, self.path)
        self.id = None

    def _prepare_shape(self, start_point, event):
        start_x, start_y = start_point
        self.width = abs(event.x - start_x)
        self.height = abs(event.y - start_y)

        self.x = int((event.x + start_x) / 2)
        self.y = int((event.y + start_y) / 2)

    def fill_image(self, file_path):
        self.image = Image.open(file_path)
        return self.image