import inspect


class Command:
    name='jump'

    def __init__(self, sketch, index=None, dx=4, dy=12, gravity=0.3, step_time=10, event=None):
        _,_,_,self.kwargs = inspect.getargvalues(inspect.currentframe())

        self.kwargs.pop('self')
        self.kwargs.pop('sketch')
        self.kwargs.pop('event')

        self.name = Command.name
        self.sketch = sketch

        if event:
            self.sketch.mark_object(event.x, event.y)
            self.kwargs['index'] = self.sketch.marked_object_index
        if self.kwargs['index'] is not None:
            self.image = self.sketch.objects[self.kwargs['index']]
            self.start_position = self.image.position
            if event and (event.x > self.start_position[0]):
                self.kwargs['dx'] = -self.kwargs['dx']
        self.start_dx = self.kwargs['dx']
        self.start_dy = self.kwargs['dy']
        self.current_dx = self.start_dx
        self.current_dy = self.start_dy

    def get_kwargs(self):
        return self.kwargs

    def on_move(self, event):
        pass

    def on_release(self, event):
        self.sketch.add_command(self)

    def do(self):
        self.current_dx = self.start_dx
        self.current_dy = self.start_dy
        if self.kwargs['index'] is None:
            return
        self.sketch.after(self.kwargs['step_time'], self._update_image)

    def undo(self):
        if self.kwargs['index'] is None:
            return
        self.image.update(position=self.start_position)

    def _update_image(self):
        new_x = self.image.position[0] + self.current_dx
        new_y = self.image.position[1] - self.current_dy

        if new_y > self.start_position[1]:
            new_y = self.start_position[1]
            self.image.update(position=(int(new_x), int(new_y)))
        else:
            self.image.update(position=(int(new_x), int(new_y)))
            self.current_dy -= self.kwargs['gravity']
            self.sketch.after(self.kwargs['step_time'], self._update_image)
