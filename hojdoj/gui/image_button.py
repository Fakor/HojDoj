import tkinter as tk
import PIL


class ImageButton(tk.Button):
    def __init__(self, parent, path, size, filler, command):
        self.raw_img = PIL.Image.open(path)
        self.size = size
        self.image_button = None
        self.parent = parent

        tk.Button.__init__(self,
                           parent,
                           command=command)
        self.update(filler)

    def update(self, filler):
        img = self.raw_img.resize(self.size, PIL.Image.NEAREST)
        img = filler.fill_image(img)

        self.image_button = PIL.ImageTk.PhotoImage(img)
        self.configure(image=self.image_button)