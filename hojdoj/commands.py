import tkinter as tk
import PIL
import tools
import sketch_object


class SketchImageCommand:
    def __init__(self, sketch, index, x, y, width,
                 height, image_name, color=None,
                 rotate=0, mirror=False, elastic_name=None):
        self.sketch = sketch
        self.index = index
        self.sketch.used_image_indexes.add(self.index)
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
        image_meta = self.sketch.config.get_first_value('image_templates', name=self.image_name)
        current_image = PIL.Image.open(image_meta['path'])
        current_image = current_image.resize((self.width, self.height), PIL.Image.NEAREST)
        if self.elastic_name:
            elastic_meta = self.sketch.config.get_first_value('image_elastics', name=self.elastic_name)
            el_image = PIL.Image.open(elastic_meta['path'])
            current_image = tools.image_replace_elastic(current_image, el_image, elastic_meta['vertical'])
        else:
            current_image = tools.image_replace_white(current_image, self.color)

        current_image = current_image.rotate(self.rotate)
        if self.mirror:
            current_image = PIL.ImageOps.mirror(current_image)
        self.image = PIL.ImageTk.PhotoImage(current_image)

        self.sketch.erase(self.index)
        self.id = self.sketch.create_image(self.x, self.y, image=self.image)
        self.sketch.objects[self.index] = sketch_object.SketchObject(self.id, self.width, self.height)

    def undo(self):
        self.sketch.delete(self.index)


class MoveImageCommand:
    def __init__(self, sketch, index, dx, dy):
        self.sketch = sketch
        self.index = index
        self.init_x, self.init_y = self.sketch.get_coords(self.index)
        self.x = self.init_x + dx
        self.y = self.init_y + dy

        self.run()

    def run(self):
        self.sketch.set_coords(self.index, self.x, self.y)

    def undo(self):
        self.sketch.set_coords(self.index, self.init_x, self.init_y)


class DeleteImageCommand:
    def __init__(self, sketch, index):
        self.sketch = sketch
        self.index = index

        self.run()

    def run(self):
        self.sketch.item_configure(self.index, state=tk.HIDDEN)

    def undo(self):
        self.sketch.item_configure(self.index, state=tk.NORMAL)


class MarkImageCommand:
    def __init__(self, sketch, x, y):
        self.sketch = sketch
        self.x = x
        self.y = y
        self.marked_before = self.sketch.marked_object_index
        self.run()

    def run(self):
        self.sketch.mark_object(self.x,self.y)

    def undo(self):
        self.sketch.marked_object_index = self.marked_before

