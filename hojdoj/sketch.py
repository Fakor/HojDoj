import tkinter as tk
import PIL

from collections import OrderedDict

from DTools.tk_tools import color_to_tk
from tools import elastic_background_horizontal
import fillers

import sketch_interactive
import image_button

import sketch_interactive
import delete_interactive
import mark_interactive
import move_interactive

interactive_commands = [
    ("Sketch", sketch_interactive.SketchInteractive),
    ("Move", move_interactive.MoveInteractive),
    ("Mark", mark_interactive.MarkInteractive),
    ("Delete", delete_interactive.DeleteInteractive)
]


class Sketch(tk.Frame):
    COLUMNS = 3

    def __init__(self, parent, config, width, height):
        tk.Frame.__init__(self, parent, width=width, height=height)
        bg_color = color_to_tk(config.get_value('background_color'))
        self.canvas = tk.Canvas(self, borderwidth=4, relief=tk.GROOVE, background=bg_color)
        self.parent = parent
        self.config = config

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.parent.bind('<Control-z>', self._undo)
        self.parent.bind('<Control-y>', self._redo)

        self.interactive_command = sketch_interactive.SketchInteractive
        self.filler = fillers.ColorFiller(self, config['default_color'])

        self.current_object = None

        self.start_point = None
        self.objects = OrderedDict()
        self.inactive_objects = []
        self.images = []

        self.current_image = self.config.get_value('image_templates', 0)
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

        canvas_width = int(width*0.87)
        canvas_height = height

        control_width = width-canvas_width
        control_height = height-canvas_height

        self.canvas.place(x=control_width, y=0, width=canvas_width, height=canvas_height)

        self.control = tk.Frame(self)

        self.B_WIDTH = int(0.94*control_width/Sketch.COLUMNS)
        self.B_HEIGHT = self.B_WIDTH

        self.interactive_row = 0
        self.interactive_col = 0

        self.image_row = 2
        self.image_col = 0

        self.color_row = 7
        self.color_col = 0

        self.elastic_row = 12
        self.elastic_col = 0

        self.normal_images = []

        self.image_buttons = []

        self.p_images = []

        for command in interactive_commands:
            self.add_interactive_command_button(*command)

        for template in config['image_templates']:
            self.add_image_button(template)

        for color in config['sketch_colors']:
            self.add_color_button(color)

        for elastic in config['image_elastics']:
            self.add_elastic_image_button(elastic)

        self.control.place(x=0, y=0, width=control_width, height=control_height)


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
            self.delete(index)

    def mark_object(self, x, y):
        for index, object in reversed(self.objects.items()):
            x2, y2 = self.canvas.coords(object.object_id)
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

    def delete(self, object_index):
        self.canvas.delete(self.objects[object_index].object_id)

    def raw_delete(self, canvas_id):
        self.canvas.delete(canvas_id)

    def create_image(self, *args, **kwargs):
        return self.canvas.create_image(*args, **kwargs)

    def get_coords(self, index):
        obj_index = self.objects[index].object_id
        return self.canvas.coords(obj_index)

    def set_coords(self, index, x, y):
        obj_index = self.objects[index].object_id
        self.canvas.coords(obj_index, x, y)

    def item_configure(self, index, *args, **kwargs):
        obj_index = self.objects[index].object_id
        self.canvas.itemconfigure(obj_index, *args, **kwargs)

    def image_tool_active(self, image_meta):
        self.current_image = image_meta
        self.interactive_command = sketch_interactive.SketchInteractive

    def color_filler_active(self, color):
        self.filler = fillers.ColorFiller(self, color)
        for button in self.image_buttons:
            button.update()

    def elastic_image_filler_active(self, elastic_meta):
        self.filler = fillers.ElasticImageFiller(self, elastic_meta)
        for button in self.image_buttons:
            button.update()

    def add_interactive_command_button(self, text, command):
        def command_func():
            self.interactive_command = command
        button = tk.Button(self, command=command_func, text=text)
        button.grid(row=self.interactive_row, column=self.interactive_col)
        if self.interactive_col == Sketch.COLUMNS - 1:
            self.interactive_col = 0
            self.interactive_row = self.interactive_row + 1
        else:
            self.interactive_col = self.interactive_col + 1

    def add_image_button(self, path):
        button = image_button.ImageButton(self, path, (self.B_WIDTH, self.B_HEIGHT))
        self.image_buttons.append(button)
        button.grid(row=self.image_row, column=self.image_col)
        if self.image_col == Sketch.COLUMNS - 1:
            self.image_col = 0
            self.image_row = self.image_row + 1
        else:
            self.image_col = self.image_col + 1

    def add_color_button(self, color):
        button = tk.Button(self, bg=color_to_tk(color), command=lambda: self.color_filler_active(color))
        button.grid(row=self.color_row, column=self.color_col)
        if self.color_col == Sketch.COLUMNS - 1:
            self.color_col = 0
            self.color_row = self.color_row + 1
        else:
            self.color_col = self.color_col + 1

    def add_elastic_image_button(self, elastic):
        path = elastic["path"]
        elastic_image = PIL.Image.open(path)
        image_button = elastic_background_horizontal(elastic_image, (self.B_WIDTH, self.B_HEIGHT))

        self.p_images.append(image_button)

        button = tk.Button(self,
                           image=self.p_images[-1],
                           command=lambda: self.elastic_image_filler_active(elastic))

        button.grid(row=self.elastic_row, column=self.elastic_col)
        if self.elastic_col == Sketch.COLUMNS - 1:
            self.elastic_col = 0
            self.elastic_row = self.elastic_row + 1
        else:
            self.elastic_col = self.elastic_col + 1
