import tkinter as tk
from sketch_image_command import SketchImageCommand, MoveImageCommand, DeleteImageCommand

import tools
import fillers

import sketch_image_tool


class Sketch(tk.Canvas):
    def __init__(self, parent, name, config, output=None):
        bg_color = tools.color_to_tk(config['background_color'])
        tk.Canvas.__init__(self, parent, borderwidth=4, relief=tk.GROOVE, background=bg_color)
        self.name = name
        self.parent = parent
        self.output = output
        self.config = config

        self.bind("<Button-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)

        self.parent.bind('<Control-z>', self._undo)
        self.parent.bind('<Control-y>', self._redo)

        self.interactive_command = sketch_image_tool.SketchImageTool
        self.filler = fillers.ColorFiller(self, config.default_color)

        self.current_object = None

        self.start_point = None
        self.objects = {}
        self.inactive_objects = []
        self.images = []

        self.current_image = self.config.image_templates[0]
        self.elastic_image = None
        self.image_index = 0
        self.used_image_indexes = set()
        self.command_index = 0
        self.commands = []

        self.move_command = None
        self.sketch_command = None
        self.delete_command = None
        self.undo_command = None
        self.redo_command = None

    def set_command_functions(self, move, sketch, delete, undo, redo):
        self.move_command = move
        self.sketch_command = sketch
        self.delete_command = delete
        self.undo_command = undo
        self.redo_command = redo

    def on_button_press(self, event):
        self.current_object = self.interactive_command(self, event)

    def on_move_press(self, event):
        self.current_object.on_move(event)

    def on_button_release(self, event):
        self.current_object.on_release(event)

    def next_image_index(self):
        while self.image_index in self.used_image_indexes:
            self.image_index = self.image_index + 1
        self.used_image_indexes.add(self.image_index)
        return self.image_index

    def undo(self, it=1):
        for i in range(it):
            self.command_index = self.command_index - 1
            self.commands[self.command_index].undo()

    def redo(self, it=1):
        for i in range(it):
            if self.command_index >= len(self.commands):
                break
            self.commands[self.command_index].run()
            self.command_index = self.command_index + 1

    def sketch_image(self, index, *args, **kwargs):
        self.commands.append(SketchImageCommand(self, index, *args, **kwargs))

    def move_image(self, index, *args, **kwargs):
        self.commands.append(MoveImageCommand(self, index, *args, **kwargs))

    def delete_image(self, index, *args, **kwargs):
        self.commands.append(DeleteImageCommand(self, index, *args, **kwargs))

    def erase(self, index):
        if index in self.objects:
            self.delete(self.objects[index])

    def _undo(self, event):
        self.undo_command()

    def _redo(self, event):
        self.redo_command()
