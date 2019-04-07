import tkinter as tk


class Sketch(tk.Canvas):
    def __init__(self, parent, width, height):
        tk.Canvas.__init__(self, parent, width=width, height=height)
        self.pack()
        self.parent = parent
        self.bind("<Button-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)

        self.parent.bind('<Control-z>', self.undo)
        self.parent.bind('<Control-y>', self.redo)

        self.paint_command = self.create_line

        self.start_point = None
        self.current_line = None

        self.objects = []
        self.inactive_objects = []

    def on_button_press(self, event):
        self.start_point = (event.x, event.y)
        self.current_line = self.paint_command(*self.start_point, *self.start_point)

    def on_move_press(self, event):
        self.coords(self.current_line, *self.start_point, event.x, event.y)

    def on_button_release(self, event):
        self.objects.append({"id": self.current_line,
                             "command": self.paint_command,
                             "cords":(*self.start_point, event.x, event.y)})

    def undo(self, event):
        if len(self.objects) != 0:
            self.delete(self.objects[-1]["id"])
            self.inactive_objects.append(self.objects.pop(-1))

    def redo(self, event):
        if len(self.inactive_objects) != 0:
            redo_obj = self.inactive_objects.pop(-1)
            new_id = redo_obj["command"](redo_obj["cords"])
            redo_obj["id"] = new_id
            self.objects.append(redo_obj)

