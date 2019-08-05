import tkinter as tk

from collections import OrderedDict

from DTools.tk_tools import color_to_tk
from DTools.main_program import MainProgram
import fillers

from DTools.button_grid import ButtonGrid

import sketch_command
import delete_command
import mark_command
import move_command

interactive_commands = [
    ("Sketch", sketch_command.SketchCommand),
    ("Move", move_command.MoveCommand),
    ("Mark", mark_command.MarkCommand),
    ("Delete", delete_command.DeleteCommand)
]


class Sketch(MainProgram):
    COLUMNS = 3

    def __init__(self, parent, config, width, height, output):
        MainProgram.__init__(self, parent, config, width, height, output)
        bg_color = color_to_tk(config.get_value('background_color'))
        self.canvas = tk.Canvas(self, borderwidth=4, relief=tk.GROOVE, background=bg_color)
        self.parent = parent

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.parent.bind('<Control-z>', self._undo)
        self.parent.bind('<Control-y>', self._redo)

        self.interactive_command = sketch_command.SketchCommand
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
        self.marked_object_index = None

        canvas_width = int(width*0.87)
        canvas_height = height

        control_width = width-canvas_width
        control_height = canvas_height

        self.canvas.place(x=control_width, y=0, width=canvas_width, height=canvas_height)

        self.control = tk.Frame(self)
        self.control.place(x=0, y=0, width=control_width, height=control_height)  # (column=0, row=0)

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
        self.color_images = []

        self.p_images = []

        for command in interactive_commands:
            self.add_interactive_command_button(*command)

        self.image_buttons = ButtonGrid(self.control, Sketch.COLUMNS, self.B_WIDTH, self.B_HEIGHT, header="Bilder", background='white')
        for image_meta in config['image_templates']:
            self.image_buttons.add_button(image_meta['path'],
                                     self.filler,
                                     self.image_tool_active,
                                     image_meta)
        self.image_buttons.grid(row=0)

        self.color_buttons = ButtonGrid(self.control, Sketch.COLUMNS, self.B_WIDTH, self.B_HEIGHT, header="Färger", background='white')
        for color in config['sketch_colors']:
            self.color_buttons.add_button(config['color_button_image_path'],
                                          fillers.ColorFiller(self, color),
                                          self.color_filler_active,
                                          color)
        self.color_buttons.grid(row=1)

        self.elastic_buttons = ButtonGrid(self.control, Sketch.COLUMNS, self.B_WIDTH, self.B_HEIGHT, header='Elastisk', background='white')
        for elastic in self.config['image_elastics']:
            self.elastic_buttons.add_button(config['color_button_image_path'],
                                            fillers.ElasticImageFiller(self, elastic),
                                            self.elastic_image_filler_active,
                                            elastic)

        self.elastic_buttons.grid(row=2)

    def on_button_press(self, event):
        self.current_object = self.interactive_command(self, x=event.x, y=event.y) #.from_event(event) #self.interactive_command(self, event)

    def on_move_press(self, event):
        self.current_object.on_move(event.x, event.y)

    def on_button_release(self, event):
        self.current_object.on_release(event.x, event.y)

    def next_image_index(self):
        while self.image_index in self.used_image_indexes:
            self.image_index = self.image_index + 1
        self.used_image_indexes.add(self.image_index)
        return self.image_index

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
        self.interactive_command = sketch_command.SketchCommand

    def color_filler_active(self, color):
        self.filler = fillers.ColorFiller(self, color)
        self.image_buttons.update_filler(self.filler)

    def elastic_image_filler_active(self, elastic_meta):
        self.filler = fillers.ElasticImageFiller(self, elastic_meta)
        self.image_buttons.update_filler(self.filler)

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
