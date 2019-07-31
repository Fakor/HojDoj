import PIL
from PIL import ImageOps
import tools
import sketch_object
import inspect


class SketchCommand:
    name = 'sketch'

    def __init__(self, sketch, index=None, x=0, y=0, image_meta=None, width=0,
                 height=0, color=None,
                 rotate=0, mirror=False, elastic_name=None):
        _,_,_,self.kwargs = inspect.getargvalues(inspect.currentframe())

        self.kwargs.pop('self')
        self.kwargs.pop('sketch')

        self.name = SketchCommand.name
        self.sketch = sketch
        self.start_x = x
        self.start_y = y
        if self.kwargs['image_meta'] is None:
            self.image_meta = self.sketch.current_image
        else:
            self.image_meta = image_meta
        self.image = None
        self.photo_image = None
        self.id = None

    def get_kwargs(self):
        return self.kwargs

    def on_move(self, x, y):
        self._prepare_shape(x, y)

        if self.id is not None:
            self.sketch.raw_delete(self.id)
        if self.kwargs['width'] == 0 or self.kwargs['height'] == 0:
            return
        self.image = PIL.Image.open(self.image_meta['path'])

        self.image = self.image.resize((self.kwargs['width'], self.kwargs['height']), PIL.Image.NEAREST)
        self.image = self.sketch.filler.fill_image(self.image)
        self.image = self.image.rotate(self.kwargs['rotate'])
        if self.kwargs['mirror']:
            self.image = ImageOps.mirror(self.image)
        self.photo_image = PIL.ImageTk.PhotoImage(self.image)
        self.id = self.sketch.create_image(self.kwargs['x'], self.kwargs['y'], image=self.photo_image)

    def on_release(self, x, y):
        self._prepare_shape(x, y)
        if self.kwargs['width'] == 0 or self.kwargs['height'] == 0:
            return
        if self.id is not None:
            self.sketch.raw_delete(self.id)
            self.sketch.filler.get_arguments(self)
            self.kwargs['index'] = self.sketch.next_image_index()
            self.sketch.add_command(self)

    def do(self):
        current_image = PIL.Image.open(self.image_meta['path'])
        current_image = current_image.resize((self.kwargs['width'], self.kwargs['height']), PIL.Image.NEAREST)
        if self.kwargs['elastic_name']:
            elastic_meta = self.sketch.config.get_first_value('image_elastics', name=self.kwargs['elastic_name'])
            el_image = PIL.Image.open(elastic_meta['path'])
            current_image = tools.image_replace_elastic(current_image, el_image, elastic_meta['vertical'])
        else:
            current_image = tools.image_replace_white(current_image, self.kwargs['color'])

        current_image = current_image.rotate(self.kwargs['rotate'])
        if self.kwargs['mirror']:
            current_image = ImageOps.mirror(current_image)
        self.image = PIL.ImageTk.PhotoImage(current_image)

        self.sketch.erase(self.kwargs['index'])
        self.id = self.sketch.create_image(self.kwargs['x'], self.kwargs['y'], image=self.image)
        self.sketch.objects[self.kwargs['index']] = sketch_object.SketchObject(self.id, self.kwargs['width'], self.kwargs['height'])

    def undo(self):
        self.sketch.erase(self.kwargs['index'])

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
