import tkinter as tk


class Sketch(tk.Canvas):
    def __init__(self, parent, width, height):
        tk.Canvas.__init__(self, parent, width=width, height=height)
        self.pack()

        self.bind("<Button-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)

        self.start_point = None
        self.current_line = None

        self.objects = []

    def on_button_press(self, event):
        self.start_point = (event.x, event.y)
        self.current_line = self.create_line(*self.start_point, *self.start_point)
        self.objects.append(self.current_line)

    def on_move_press(self, event):
        self.coords(self.current_line, *self.start_point, event.x, event.y)

    def on_button_release(self, event):
        pass