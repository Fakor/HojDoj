from DTools.sketch_image import SketchImage
import DTools.fillers


class Command:
    name = 'sketch'

    def __init__(self, sketch, index=None, event=None, image_name=None,
                 pos=(0,0), size=(0,0), color=None,
                 rotate=0, mirror=False, elastic_name=None):
        self.name = Command.name
        self.sketch = sketch
        if event:
            self.start_pos = (event.x, event.y)
        self.pos = pos
        if image_name is None:
            self.image_meta = self.sketch.current_image
        else:
            self.image_meta = self.sketch.config.get_first_value('image_templates', name=image_name)
        self.index = index
        self.size = size
        self.mirror = mirror
        self.rotate = rotate
        self.elastic_name = elastic_name
        self.color = color

        if color is not None:
            self.filler = DTools.fillers.ColorFiller(color)
        elif elastic_name is not None:
            elastic_meta = self.sketch.config.get_first_value('image_elastics', name=elastic_name)
            self.filler = DTools.fillers.ElasticImageFiller(elastic_meta)
        else:
            self.filler = sketch.filler

        self.filler.get_arguments(self)
        try:
            self.orig_image = self.sketch.objects[self.index]
        except KeyError:
            self.orig_image = None
        self.image = SketchImage(sketch,
                                 self.image_meta['path'],
                                 self.pos,
                                 self.size,
                                 filler=self.filler,
                                 rotate=rotate,
                                 mirror=mirror)

    def get_kwargs(self):
        return {
            'index': self.index,
            'image_name': self.image_meta['name'],
            'pos': self.pos,
            'size': self.size,
            'rotate': self.rotate,
            'mirror': self.mirror,
            'color': self.color,
            'elastic_name': self.elastic_name
        }

    def on_move(self, event):
        self._prepare_shape(event.x, event.y)
        self._update_image()

    def on_release(self, event):
        self._prepare_shape(event.x, event.y)
        if any(el == 0 for el in self.size):
            return
        self.index = self.sketch.next_image_index()
        self.sketch.add_command(self)

    def do(self):
        if self.orig_image is not None:
            self.orig_image.hide()
        self._update_image()
        self.sketch.objects[self.index] = self.image

    def undo(self):
        if self.orig_image is not None:
            self.orig_image.show()
        self.image.hide()

    def _prepare_shape(self, x, y):
        self.size = (abs(x - self.start_pos[0]), abs(y - self.start_pos[1]))

        if y < self.start_pos[1]:
            self.rotate = 180
            self.mirror = x > self.start_pos[0]
        else:
            self.rotate = 0
            self.mirror = x < self.start_pos[0]
        new_x = int((x + self.start_pos[0]) / 2)
        new_y = int((y + self.start_pos[1]) / 2)
        self.pos = (new_x, new_y)

    def _update_image(self):
        self.image.update(position=self.pos,
                          size=self.size,
                          rotate=self.rotate,
                          mirror=self.mirror)
