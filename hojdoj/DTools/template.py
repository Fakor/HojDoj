import tkinter as tk

from DTools.command_terminal import CommandTerminal
from DTools.command_basics import command_from_meta


class Template(tk.Frame):
    def __init__(self, parent, main_init, config, position, size, shell_locals):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.bind('<Control-c>', self.quit)

        width, height = size

        output_window_height = int(height/25)
        self.output_panel = CommandTerminal(self, shell_locals)
        self.control_panel = tk.Frame(self)
        self.control_button_row = 0
        self.control_button_column = 0

        control_width = int(width/20)

        main_height = height-output_window_height
        main_width = width - control_width

        self.main = main_init(self, config, position, (main_width, main_height), self.output_panel)

        self.main.place(x=0, y=0, width=main_width, height=main_height)
        self.output_panel.place(x=0, y=main_height, width=width, height=main_height)
        self.control_panel.place(x=main_width, y=0, width=control_width, height=main_height)

    def add_control_button(self, command, text=None):
        button = tk.Button(self.control_panel, command=command, text=text)
        button.grid(row=self.control_button_row, column=self.control_button_column)
        self.control_button_row = self.control_button_row+1

    def update_locals(self, new_locals):
        self.output_panel.update_locals(new_locals)

    def quit(self, event):
        self.parent.event_generate('<<quit_now>>')

    def init_command(self, command):
        def func(*args, **kwargs):
            c = command(self.main, *args, **kwargs)
            self.main.add_command(c)
        self.output_panel.add_local(command.name, func)

    def init_commands(self, commands):
        for command_meta in commands:
            self.init_command(command_from_meta(command_meta))
