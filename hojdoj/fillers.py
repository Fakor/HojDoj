from PIL import Image

from tools import elastic_background, image_replace_white, image_replace_elastic
from tools import Colors


class ColorFiller:
    def __init__(self, sketch, color):
        self.sketch = sketch
        self.color = color
        self.id = None
        self.image = None

    def update_rect(self, start_point, event):
        args = (*start_point, event.x, event.y)
        if self.id is None:
            self.id = self.sketch.create_rectangle(*args, fill=self.color['tk'])
        else:
            self.sketch.coords(self.id, *args)

    def make_rect_sketch(self, start_point, event):
        if self.id is not None:
            self.sketch.delete(self.id)
            self.sketch.sketch_rect(*start_point, event.x, event.y, fill=self.color['tk'])
        self.id = None

    def fill_image(self, image):
        return image_replace_white(image, self.color['RGB'])

    def get_arguments(self, event, start_point):
        self._prepare_shape(start_point, event)
        return {'color': self.color['RGB'], 'rotate': self.rotate, 'mirror': self.mirror}

    def _prepare_shape(self, start_point, event):
        start_x, start_y = start_point
        self.width = abs(event.x - start_x)
        self.height = abs(event.y - start_y)

        if event.y < start_y:
            self.rotate = 180
            if event.x > start_x:
                self.mirror = True
            else:
                self.mirror = False
        else:
            self.rotate = 0
            if event.x < start_x:
                self.mirror = True
            else:
                self.mirror = False

        self.x = int((event.x + start_x) / 2)
        self.y = int((event.y + start_y) / 2)


class ElasticImageFiller:
    def __init__(self, sketch, path):
        self.sketch = sketch
        self.path = path
        self.elastic_image = Image.open(self.path)

        self.image = None
        self.id =None
        self.color = Colors.WHITE

    def update_rect(self, start_point, event):
        self._prepare_shape(start_point, event)
        if self.id is not None:
            self.sketch.delete(self.id)
        if self.width == 0 or self.height == 0:
            return
        self.image = elastic_background(self.elastic_image, (self.width, self.height))
        self.id = self.sketch.create_image(self.x, self.y, image=self.image)

    def make_rect_sketch(self, start_point, event, id):
        if id is not None:
            self._prepare_shape(start_point, event)
            if self.width == 0 or self.height == 0:
                return
            self.sketch.delete(self.id)
            self.sketch.sketch_elastic_image(self.x, self.y, self.width, self.height, self.path, self.elastic_path)

    def _prepare_shape(self, start_point, event):
        start_x, start_y = start_point
        self.width = abs(event.x - start_x)
        self.height = abs(event.y - start_y)

        if event.y < start_y:
            self.rotate = 180
            if event.x > start_x:
                self.mirror = True
            else:
                self.mirror = False
        else:
            self.rotate = 0
            if event.x < start_x:
                self.mirror = True
            else:
                self.mirror = False

        self.x = int((event.x + start_x) / 2)
        self.y = int((event.y + start_y) / 2)

    def fill_image(self, image):
        return image_replace_elastic(image, self.elastic_image)

    def get_arguments(self, event, start_point):
        self._prepare_shape(start_point, event)
        return {'elastic_image_path': self.path, 'rotate': self.rotate, 'mirror': self.mirror}
