import tkinter as tk

from decorators import call_syntax


class Sketch(tk.Canvas):
    def __init__(self, parent, width, height, name, output=None):
        tk.Canvas.__init__(self, parent, width=width, height=height)
        self.name = name
        self.grid()
        self.parent = parent
        self.output = output
        self.bind("<Button-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)

        self.parent.bind('<Control-z>', self._undo)
        self.parent.bind('<Control-y>', self._redo)

        self.paint_command = "line"

        self.start_point = None
        self.current_object = None

        self.objects = []
        self.inactive_objects = []

    def on_button_press(self, event):
        self.start_point = (event.x, event.y)
        self.current_object = self.current_tk_paint_command(*self.start_point, *self.start_point)

    def on_move_press(self, event):
        self.coords(self.current_object, *self.start_point, event.x, event.y)

    def on_button_release(self, event):
        self.delete(self.current_object)
        self.current_sketch_command(*self.start_point, event.x, event.y)

    @call_syntax
    def undo(self):
        if len(self.objects) != 0:
            self.delete(self.objects[-1]["id"])
            self.inactive_objects.append(self.objects.pop(-1))

    @call_syntax
    def redo(self):
        if len(self.inactive_objects) != 0:
            redo_obj = self.inactive_objects.pop(-1)
            new_id = redo_obj["command"](redo_obj["cords"])
            redo_obj["id"] = new_id
            self.objects.append(redo_obj)

    @call_syntax
    def sketch_line(self, x1, y1, x2, y2):
        new_id = self.current_tk_paint_command(x1, y1, x2, y2)
        self.objects.append({"id": new_id,
                             "command": self.current_tk_paint_command,
                             "cords":(x1, y1, x2, y2)})

    @call_syntax
    def sketch_rect(self, x1, y1, x2, y2):
        new_id = self.current_tk_paint_command(x1, y1, x2, y2)
        self.objects.append({"id": new_id,
                             "command": self.current_tk_paint_command,
                             "cords":(x1, y1, x2, y2)})

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

