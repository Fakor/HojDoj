import inspect
from DTools.sketch_image import SketchImage
import DTools.fillers


class Command:
    name = 'sketch'

    def __init__(self, sketch, index=None, event=None, image_meta=None,
                 x=0, y=0, width=0,
                 height=0, color=None,
                 rotate=0, mirror=False, elastic_name=None):
        _,_,_,self.kwargs = inspect.getargvalues(inspect.currentframe())

        self.kwargs.pop('self')
        self.kwargs.pop('sketch')
        self.kwargs.pop('event')

        self.name = Command.name
        self.sketch = sketch
        if event:
            self.start_x = event.x
            self.start_y = event.y
        else:
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
        try:
            self.orig_image = self.sketch.objects[self.kwargs['index']]
        except KeyError:
            self.orig_image = None
        self.image = SketchImage(sketch,
                                 self.image_meta['path'],
                                 (self.start_x, self.start_y),
                                 (width, height),
                                 filler=self.filler,
                                 rotate=rotate,
                                 mirror=mirror)

    def get_kwargs(self):
        return self.kwargs

    def on_move(self, event):
        self._prepare_shape(event.x, event.y)
        self._update_image()

    def on_release(self, event):
        self._prepare_shape(event.x, event.y)
        if self.kwargs['width'] == 0 or self.kwargs['height'] == 0:
            return
        self.kwargs['index'] = self.sketch.next_image_index()
        self.sketch.add_command(self)

    def do(self):
        if self.orig_image is not None:
            self.orig_image.hide()
        self._update_image()
        self.sketch.objects[self.kwargs['index']] = self.image

    def undo(self):
        if self.orig_image is not None:
            self.orig_image.show()
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
