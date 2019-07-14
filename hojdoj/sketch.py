import tkinter as tk

from collections import OrderedDict

import tools
import fillers

import sketch_interactive


class Sketch(tk.Canvas):
    def __init__(self, parent, config, output=None):
        bg_color = tools.color_to_tk(config['background_color'])
        tk.Canvas.__init__(self, parent, borderwidth=4, relief=tk.GROOVE, background=bg_color)
        self.parent = parent
        self.output = output
        self.config = config

        self.bind("<Button-1>", self.on_button_press)
        self.bind("<B1-Motion>", self.on_move_press)
        self.bind("<ButtonRelease-1>", self.on_button_release)

        self.parent.bind('<Control-z>', self._undo)
        self.parent.bind('<Control-y>', self._redo)

        self.interactive_command = sketch_interactive.SketchInteractive
        self.filler = fillers.ColorFiller(self, config.default_color)

        self.current_object = None

        self.start_point = None
        self.objects = OrderedDict()
        self.inactive_objects = []
        self.images = []

        self.current_image = self.config.image_templates[0]
        self.elastic_image = None
        self.image_index = 0
        self.used_image_indexes = set()
        self.command_index = 0
        self.commands = []
        self.marked_object_index = None

        self.move_command = None
        self.sketch_command = None
        self.delete_command = None
        self.undo_command = None
        self.redo_command = None
        self.mark_command = None

    def set_command_functions(self, move, sketch, delete, mark, undo, redo):
        self.move_command = move
        self.sketch_command = sketch
        self.delete_command = delete
        self.undo_command = undo
        self.redo_command = redo
        self.mark_command = mark

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

    def add_command(self, command, *args, **kwargs):
        self.commands.append(command(self, *args, **kwargs))

    def erase(self, index):
        if index in self.objects:
            self.delete(self.objects[index])

    def mark_object(self, x, y):
        for index, object in reversed(self.objects.items()):
            x2, y2 = self.coords(object.object_id)
            width_half = object.width/2
            height_half = object.height/2
            if (x2-width_half <= x <= x2 + width_half) and (y2-height_half<= y <= y2 + height_half):
                self.marked_object_index = index
                return
        self.marked_object_index = None

    def _undo(self, event):
        self.undo_command()

    def _redo(self, event):
        self.redo_command()
