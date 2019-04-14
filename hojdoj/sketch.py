import tkinter as tk
from PIL import Image, ImageTk

from decorators import base_call, object_call


class Sketch(tk.Canvas):
    def __init__(self, parent, width, height, name, image_root, output=None):
        tk.Canvas.__init__(self, parent, width=width, height=height)
        self.name = name
        self.grid()
        self.parent = parent
        self.output = output
        self.image_root = image_root
        self.bind("<Button-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)

        self.parent.bind('<Control-z>', self._undo)
        self.parent.bind('<Control-y>', self._redo)

        self.paint_command = "line"
        self.color = "red"

        self.current_image = Image.open("{}/baltazar.png".format(image_root))
        self.img = ImageTk.PhotoImage(self.current_image)
        self.start_point = None
        self.current_object = None

        self.objects = []
        self.inactive_objects = []

    def on_button_press(self, event):
        self.start_point = (event.x, event.y)
        self.current_object = self.current_tk_paint_command(*self.start_point, *self.start_point, fill=self.color)

    def on_move_press(self, event):
        self.coords(self.current_object, *self.start_point, event.x, event.y)

    def on_button_release(self, event):
        self.delete(self.current_object)
        self.current_sketch_command(*self.start_point, event.x, event.y, fill=self.color)

    @base_call
    def undo(self):
        if len(self.objects) != 0:
            self.delete(self.objects[-1]["id"])
            self.inactive_objects.append(self.objects.pop(-1))

    @base_call
    def redo(self):
        if len(self.inactive_objects) != 0:
            redo_obj = self.inactive_objects.pop(-1)
            new_id = redo_obj["command"](self, *redo_obj["args"], **redo_obj["kwargs"])
            redo_obj["id"] = new_id
            self.objects.append(redo_obj)

    @object_call(tk.Canvas.create_line)
    def sketch_line(self, x1, y1, x2, y2, **kwargs):
        pass

    @object_call(tk.Canvas.create_rectangle)
    def sketch_rect(self, x1, y1, x2, y2, **kwargs):
        pass

    def sketch_current_image(self, x1, y1):
        new_id = self.create_image(x1, y1, image=self.img)
        self.objects.append({"id": new_id,
                             "command": self.sketch_current_image,
                             "args":(x1, y1)})

    def _undo(self, event):
        self.undo()

    def _redo(self, event):
        self.redo()

    @property
    def current_tk_paint_command(self):
        if self.paint_command == "line":
            return self.create_line
        elif self.paint_command == "rect":
            return self.create_rectangle
        else:
            return None

    @property
    def current_sketch_command(self):
        if self.paint_command == "line":
            return self.sketch_line
        elif self.paint_command == "rect":
            return self.sketch_rect
        else:
            return None

