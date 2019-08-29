from logic.image_logic import ImageLogic


class Command:
    def __init__(self, sketch, event, command_name):
        self.sketch = sketch
        self.image_name = self.sketch.current_image
        self.command_name = command_name
        self.start_pos = (event.x, event.y)
        self.pos = self.start_pos
        self.size = (0,0)
        self.image = ImageLogic(self.sketch.get_image_path(self.image_name), self.pos, self.size)

    def on_move(self, event):
        self._prepare_shape(event.x, event.y)
        self.image.update(size=self.size, position=self.pos)
        self.sketch.create_temporary_image(self.image)

    def on_release(self, event):
        self._prepare_shape(event.x, event.y)
        if any(el == 0 for el in self.size):
            return
        self.sketch.new_command(self.command_name,
                                self.image_name,
                                self.pos,
                                self.size)

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