import inspect
from DTools.sketch_image import SketchImage
import DTools.fillers


class Command:
    name = 'sketch'

    def __init__(self, sketch, index=None, x=0, y=0, image_meta=None, width=0,
                 height=0, color=None,
                 rotate=0, mirror=False, elastic_name=None):
        _,_,_,self.kwargs = inspect.getargvalues(inspect.currentframe())

        self.kwargs.pop('self')
        self.kwargs.pop('sketch')

        self.name = Command.name
        self.sketch = sketch
        self.start_x = x
        self.start_y = y
        if self.kwargs['image_meta'] is None:
            self.image_meta = self.sketch.current_image
        else:
            self.image_meta = image_meta

        if color is not None:
            self.filler = DTools.fillers.ColorFiller(color)
        elif elastic_name is not None:
            elastic_meta = self.sketch.config.get_first_value('image_elastics', name=elastic_name)
            self.filler = DTools.fillers.ElasticImageFiller(elastic_meta)
        else:
            self.filler = sketch.filler

        self.filler.get_arguments(self)
        self.image = SketchImage(sketch,
                                 self.image_meta['path'],
                                 (x,y),
                                 (width, height),
                                 filler=self.filler,
                                 rotate=rotate,
                                 mirror=mirror)

    def get_kwargs(self):
        return self.kwargs

    def on_move(self, x, y):
        self._prepare_shape(x, y)
        self._update_image()

    def on_release(self, x, y):
        self._prepare_shape(x, y)
        if self.kwargs['width'] == 0 or self.kwargs['height'] == 0:
            return
        self.kwargs['index'] = self.sketch.next_image_index()
        self.sketch.add_command(self)

    def do(self):
        self._update_image()
        self.sketch.objects[self.kwargs['index']] = self.image #sketch_object.SketchObject(self.id, self.kwargs['width'], self.kwargs['height'])

    def undo(self):
        self.image.hide()

    def _prepare_shape(self, x, y):
        self.kwargs['width'] = abs(x - self.start_x)
        self.kwargs['height'] = abs(y - self.start_y)

        if y < self.start_y:
            self.kwargs['rotate'] = 180
            self.kwargs['mirror'] = x > self.start_x
        else:
            self.kwargs['rotate'] = 0
            self.kwargs['mirror'] = x < self.start_x
        self.kwargs['x'] = int((x + self.start_x) / 2)
        self.kwargs['y'] = int((y + self.start_y) / 2)

    def _get_image_position(self):
        return self.kwargs['x'], self.kwargs['y']

    def _get_image_size(self):
        return self.kwargs['width'], self.kwargs['height']

    def _get_image_rotate(self):
        return self.kwargs['rotate']

    def _get_image_mirror(self):
        return self.kwargs['mirror']

    def _update_image(self):
        self.image.update(position=self._get_image_position(),
                          size=self._get_image_size(),
                          rotate=self._get_image_rotate(),
                          mirror=self._get_image_mirror())
