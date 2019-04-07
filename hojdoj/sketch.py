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

        self.start_point = None
        self.current_line = None

        self.objects = []
        self.inactive_objects = []

    def on_button_press(self, event):
        self.start_point = (event.x, event.y)
        self.current_line = self.create_line(*self.start_point, *self.start_point)
        self.objects.append(self.current_line)

    def on_move_press(self, event):
        self.coords(self.current_line, *self.start_point, event.x, event.y)

    def on_button_release(self, event):
        pass

    def undo(self, event):
        if len(self.objects) != 0:
            self.delete(self.objects[-1])
            self.inactive_objects.append(self.objects.pop(-1))