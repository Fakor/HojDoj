from PIL import Image

from DTools.tools import image_replace_white, image_replace_elastic


class ColorFiller:
    def __init__(self, color):
        self.color = color
        self.id = None
        self.image = None

    def fill_image(self, image):
        return image_replace_white(image, self.color)

    def get_arguments(self, command):
        command.color = self.color


class ElasticImageFiller:
    def __init__(self, path, vertical):
        self.elastic_image = Image.open(path)
        self.vertical = vertical
        self.image = None
        self.id =None

    def fill_image(self, image):
        return image_replace_elastic(image, self.elastic_image, self.vertical)


class NoFiller:
    def __init__(self):
        pass

    def fill_image(self, image):
        return image

    def get_arguments(self, command):
        pass