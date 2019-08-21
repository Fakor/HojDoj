import tkinter as tk

from image_button import ImageButton


class ButtonGrid(tk.Frame):
    def __init__(self, parent, columns, button_width, button_height, header=None, background=None):
        self.columns = columns
        self.size = (button_width, button_height)

        self.width = self.columns * button_width
        tk.Frame.__init__(self, parent, width=self.width, bg=background)
        self.parent = parent

        label = tk.Label(self, text=header, anchor=tk.CENTER, bg=background)
        label.grid(row=0, columnspan=self.columns)

        self.current_row = 1
        self.current_column = 0
        self.buttons = []

    def add_button(self, path, filler, command, *command_args, **command_kwargs):
        button = ImageButton(self, path, self.size, filler, lambda: command(*command_args, **command_kwargs))

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
