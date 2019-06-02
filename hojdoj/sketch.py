import tkinter as tk
from PIL import Image, ImageTk, ImageOps

import tools
import fillers

import Commands


class Sketch(tk.Canvas):
    def __init__(self, parent, name, default_image, config, output=None):
        tk.Canvas.__init__(self, parent)
        self.name = name
        self.parent = parent
        self.output = output
        self.bind("<Button-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)

        self.parent.bind('<Control-z>', self._undo)
        self.parent.bind('<Control-y>', self._redo)

        self.interactive_command = Commands.SketchImageInteractive
        self.filler = fillers.ColorFiller(self, config.default_color)

        self.current_object = None

        self.start_point = None
        self.objects = []
        self.inactive_objects = []
        self.images = []

        self.current_image = default_image
        self.elastic_image = None

    def on_button_press(self, event):
        self.current_object = self.interactive_command(self, event)

    def on_move_press(self, event):
        self.current_object.on_move(event)

    def on_button_release(self, event):
        self.current_object.on_release(event)

    @tools.base_call
    def undo(self, it=1):
        for i in range(it):
            if len(self.objects) != 0:
                self.delete(self.objects[-1]['id'])
                self.inactive_objects.append(self.objects.pop(-1))

    @tools.base_call
    def redo(self, it=1):
        for i in range(it):
            if len(self.inactive_objects) != 0:
                redo_obj = self.inactive_objects.pop(-1)
                new_id = redo_obj["command"](self, *redo_obj["args"], **redo_obj["kwargs"])
                redo_obj["id"] = new_id
                self.objects.append(redo_obj)

    def _sketch_image(self, x, y, width,
                      height, path, color=None,
                      rotate=0, mirror=False, elastic_image_path=None,
                      vertical=False):
        current_image = Image.open(path)

        current_image = current_image.resize((width, height), Image.NEAREST)
        if elastic_image_path:
            el_image = Image.open(elastic_image_path)
            current_image = tools.image_replace_elastic(current_image, el_image, vertical)
        else:
            current_image = tools.image_replace_white(current_image, color)

        current_image = current_image.rotate(rotate)
        if mirror:
            current_image = ImageOps.mirror(current_image)
        self.images.append(ImageTk.PhotoImage(current_image))
        return self.create_image(x, y, image=self.images[-1])

    @tools.object_call(_sketch_image)
    def sketch_image(self, *args, **kwargs):
        pass

    def _undo(self, event):
        self.undo()

    def _redo(self, event):
        self.redo()
