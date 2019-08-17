import inspect


class Command:
    name='jump'

    def __init__(self, sketch, index=None, dx=0, dy=0, gravity=0.3, step_time=20, x=0,y=0):
        _,_,_,self.kwargs = inspect.getargvalues(inspect.currentframe())

        self.kwargs.pop('self')
        self.kwargs.pop('sketch')
        self.kwargs.pop('x')
        self.kwargs.pop('y')

        self.name = Command.name
        self.sketch = sketch

        if self.kwargs['index'] is None:
            self.sketch.mark_object(x, y)
            self.kwargs['index'] = self.sketch.marked_object_index
        if self.kwargs['index'] is not None:
            self.image = self.sketch.objects[self.kwargs['index']]
            self.start_position = self.image.position
        self.current_dx = dx
        self.current_dy = dy

    def get_kwargs(self):
        return self.kwargs

    def do(self):
        if self.kwargs['index'] is None:
            return
        self.sketch.after(self.kwargs['step_time'], self._update_image)

    def undo(self):
        if self.kwargs['index'] is None:
            return
        self.image.set_position(position=self.start_position)

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
