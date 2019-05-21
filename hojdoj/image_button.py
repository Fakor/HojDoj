import tkinter as tk
import PIL


class ImageButton(tk.Button):
    def __init__(self, parent, path, size):
        self.raw_img = PIL.Image.open(path)
        self.size = size
        self.image_button = None
        self.parent = parent
        self.path = path

        tk.Button.__init__(self,
                           parent,
                           command=lambda: parent.image_tool_active(path))
        self.update()

    def update(self):
        img = self.raw_img.resize(self.size, PIL.Image.NEAREST)
        img = self.parent.sketch.filler.fill_image(img)


        self.image_button = PIL.ImageTk.PhotoImage(img)
        self.configure(image=self.image_button)