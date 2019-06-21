import tkinter as tk
from sketch_image_command import SketchImageCommand

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
        self.commands = {}
        self.inactive_objects = []
        self.images = []

        self.current_image = self.config.image_templates[0]
        self.elastic_image = None
        self.image_index = 0

    def on_button_press(self, event):
        self.current_object = self.interactive_command(self, event)

    def on_move_press(self, event):
        self.current_object.on_move(event)

    def on_button_release(self, event):
        self.current_object.on_release(event)

    def next_image_index(self):
        self.image_index = self.image_index + 1
        return self.image_index

    @tools.base_call
    def undo(self, it=1):
        pass

    @tools.base_call
    def redo(self, it=1):
        pass

    @tools.base_call
    def sketch_image(self, index, *args, **kwargs):
        if index in self.commands:
            self.commands[index].update(*args, **kwargs)
        else:
            self.commands[index] = SketchImageCommand(self, *args, **kwargs)

    def _undo(self, event):
        self.undo()

    def _redo(self, event):
        self.redo()
