from DTools.base_command import BaseCommand


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.image_name = self.logic.current_image
        self.pos = (self.init_event.x, self.init_event.y)
        self.size = (0,0)
        self.rotation = 0
        self.mirror = False
        self.index = self.logic.next_image_index()

    def on_move(self, event):
        self._prepare_shape(event.x, event.y)
        self.logic.draw_object(self.image_name, self.pos, self.size, **self.kwargs)

    def on_release(self, event):
        self._prepare_shape(event.x, event.y)
        if any(el == 0 for el in self.size):
            return
        self.perform_command(self.name,
                             self.image_name,
                             self.pos,
                             self.size,
                             **self.kwargs)

    def _prepare_shape(self, x, y):
        self.size = (abs(x - self.init_event.x), abs(y - self.init_event.y))

        if y < self.init_event.y:
            self.rotation = 180
            self.mirror = x > self.init_event.x
        else:
            self.rotation = 0
            self.mirror = x < self.init_event.x
        new_x = int((x + self.init_event.x) / 2)
        new_y = int((y + self.init_event.y) / 2)
        self.pos = (new_x, new_y)

    @property
    def kwargs(self):
        kwargs = {}
        if self.index is not None:
            kwargs['index'] = self.index
        if self.rotation is not 0:
            kwargs['rotation'] = self.rotation
        if self.mirror:
            kwargs['mirror'] = self.mirror
        kwargs['filler'] = self.logic.current_filler
        return kwargs