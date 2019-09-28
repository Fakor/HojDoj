import tkinter as tk
import PIL


class ButtonGrid(tk.Frame):
    def __init__(self, parent, columns, button_width, button_height, header=None, background=None):
        self.columns = columns
        self.size = (button_width, button_height)
        self.background = background
        self.width = self.columns * button_width
        tk.Frame.__init__(self, parent, width=self.width, bg=background)
        self.parent = parent

        label = tk.Label(self, text=header, anchor=tk.CENTER, bg=background)
        label.grid(row=0, columnspan=self.columns)

        self.current_row = 1
        self.current_column = 0
        self.buttons = []

    def add_button(self, path, filler, command, *command_args, **command_kwargs):
        button = ImageButton(self, path, self.size, filler, self.background, lambda: command(*command_args, **command_kwargs))

        button.grid(row=self.current_row, column=self.current_column)
        self.buttons.append(button)
        if self.current_column == self.columns - 1:
            self.current_column = 0
            self.current_row = self.current_row + 1
        else:
            self.current_column = self.current_column + 1

    def update_filler(self, filler):
        for button in self.buttons:
            button.update(filler)

    def remove_highlights(self):
        for button in self.buttons:
            button.configure(highlightbackground=self.background)


class ImageButton(tk.Button):
    def __init__(self, parent, path, size, filler, background, command):
        self.raw_img = PIL.Image.open(path)
        self.size = size
        self.image_button = None
        self.parent = parent
        self.command = command
        tk.Button.__init__(self,
                           parent,
                           command=self.pressed,
                           highlightbackground=background)
        self.update(filler)

    def update(self, filler):
        img = self.raw_img.resize(self.size, PIL.Image.NEAREST)
        img = filler.fill_image(img)

        self.image_button = PIL.ImageTk.PhotoImage(img)
        self.configure(image=self.image_button)

    def pressed(self):
        self.parent.remove_highlights()
        self.configure(highlightbackground='red')
        self.command()