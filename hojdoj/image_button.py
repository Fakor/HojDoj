import tkinter as tk
import PIL


class ImageButton(tk.Button):
    def __init__(self, parent, path, size):
        self.img = PIL.Image.open(path)
        self.img = parent.sketch.filler.fill_image(self.img)
        self.img = self.img.resize(size, PIL.Image.ANTIALIAS)
        self.image_button = PIL.ImageTk.PhotoImage(self.img)

        tk.Button.__init__(self,
                           parent,
                           image=self.image_button,
                           command=lambda: parent.image_tool_active(path))
        self.parent = parent
        self.path = path
