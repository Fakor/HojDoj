import PIL
import tools


class SketchImageCommand:
    def __init__(self, sketch, index, x, y, width,
                 height, image_name, color=None,
                 rotate=0, mirror=False, elastic_name=None):
        self.sketch = sketch
        self.index = index
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_name = image_name
        self.color = color
        self.rotate = rotate
        self.mirror = mirror
        self.elastic_name = elastic_name

        self.image = None
        self.id = None
        self.run()

    def run(self):
        image_meta = self.sketch.config.get_image_meta(self.image_name)
        current_image = PIL.Image.open(image_meta['path'])
        current_image = current_image.resize((self.width, self.height), PIL.Image.NEAREST)
        if self.elastic_name:
            elastic_meta = self.sketch.config.get_elastic_meta(self.elastic_name)
            el_image = PIL.Image.open(elastic_meta['path'])
            current_image = tools.image_replace_elastic(current_image, el_image, elastic_meta['vertical'])
        else:
            current_image = tools.image_replace_white(current_image, self.color)

        current_image = current_image.rotate(self.rotate)
        if self.mirror:
            current_image = PIL.ImageOps.mirror(current_image)
        self.image = PIL.ImageTk.PhotoImage(current_image)

        self.id = self.sketch.create_image(self.x, self.y, image=self.image)
        self.sketch.objects[self.index] = self.id

    def undo(self):
        self.sketch.delete(self.sketch.objects[self.index])
