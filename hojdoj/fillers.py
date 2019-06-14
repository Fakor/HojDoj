from PIL import Image

from tools import image_replace_white, image_replace_elastic


class ColorFiller:
    def __init__(self, sketch, color):
        self.sketch = sketch
        self.color = color
        self.id = None
        self.image = None

    def fill_image(self, image):
        return image_replace_white(image, self.color)

    def get_arguments(self, event, start_point):
        self._prepare_shape(start_point, event)
        return {'color': self.color, 'rotate': self.rotate, 'mirror': self.mirror}

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
    def __init__(self, sketch, elastic_meta):
        self.sketch = sketch
        self.meta = elastic_meta
        self.elastic_image = Image.open(self.meta['path'])

        self.image = None
        self.id =None

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
        return image_replace_elastic(image, self.elastic_image, self.meta['vertical'])

    def get_arguments(self, event, start_point):
        self._prepare_shape(start_point, event)
        return {'elastic_name': self.meta['name'], 'rotate': self.rotate, 'mirror': self.mirror}
