import tkinter as tk
from tkinter import filedialog
import pyscreenshot
from collections import OrderedDict

from DTools.tk_tools import color_to_tk
from DTools.main_program import MainProgram
from DTools.command_basics import command_from_meta
from DTools import fillers

from DTools.button_grid import ButtonGrid

from commands import sketch


class Sketch(MainProgram):
    COLUMNS = 3

    def __init__(self, parent, config, position, size, output):
        width, height = size
        MainProgram.__init__(self, parent, config, width, height, output)
        bg_color = color_to_tk(config.get_value('background_color'))
        self.canvas = tk.Canvas(self, borderwidth=4, relief=tk.GROOVE, background=bg_color)
        self.parent = parent
        self.position = position

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.parent.bind('<Control-z>', self._undo)
        self.parent.bind('<Control-y>', self._redo)

        self.interactive_command = sketch.Command
        self.filler = fillers.ColorFiller(config['default_color'])

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
        self.control.place(x=0, y=0, width=control_width, height=control_height)

        self.B_WIDTH = int(0.94*control_width/Sketch.COLUMNS)
        self.B_HEIGHT = self.B_WIDTH

        x, y = size
        self.canvas_position = x, 0
        self.canvas_size = canvas_width, canvas_height


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

        self.command_buttons = ButtonGrid(self.control, Sketch.COLUMNS, self.B_WIDTH, self.B_HEIGHT, header="Commands", background='white')
        for command_meta in config['commands']:
            self.command_buttons.add_button(command_meta['image'],
                                            fillers.NoFiller(),
                                            self.set_interactive_command,
                                            command_meta)
        self.command_buttons.grid(row=0)

        self.image_buttons = ButtonGrid(self.control, Sketch.COLUMNS, self.B_WIDTH, self.B_HEIGHT, header="Bilder", background='white')
        for image_meta in config['image_templates']:
            self.image_buttons.add_button(image_meta['path'],
                                          self.filler,
                                          self.image_tool_active,
                                          image_meta)
        self.image_buttons.grid(row=1)

        self.color_buttons = ButtonGrid(self.control, Sketch.COLUMNS, self.B_WIDTH, self.B_HEIGHT, header="Färger", background='white')
        for color in config['sketch_colors']:
            self.color_buttons.add_button(config['color_button_image_path'],
                                          fillers.ColorFiller(color),
                                          self.color_filler_active,
                                          color)
        self.color_buttons.grid(row=2)

        self.elastic_buttons = ButtonGrid(self.control, Sketch.COLUMNS, self.B_WIDTH, self.B_HEIGHT, header='Elastisk', background='white')
        for elastic in self.config['image_elastics']:
            self.elastic_buttons.add_button(config['color_button_image_path'],
                                            fillers.ElasticImageFiller(elastic),
                                            self.elastic_image_filler_active,
                                            elastic)

        self.elastic_buttons.grid(row=3)

    def on_button_press(self, event):
        self.current_object = self.interactive_command(self, x=event.x, y=event.y)

    def on_move_press(self, event):
        self.current_object.on_move(event.x, event.y)

    def on_button_release(self, event):
        self.current_object.on_release(event.x, event.y)

    def next_image_index(self):
        while self.image_index in self.used_image_indexes:
            self.image_index = self.image_index + 1
        self.used_image_indexes.add(self.image_index)
        return self.image_index

    def mark_object(self, x, y):
        for index, object in reversed(self.objects.items()):
            if object.cover_position(x,y):
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

    def set_coords(self, id, x, y):
        self.canvas.coords(id, x, y)

    def item_configure(self, id, *args, **kwargs):
        self.canvas.itemconfigure(id, *args, **kwargs)

    def image_tool_active(self, image_meta):
        self.current_image = image_meta
        self.interactive_command = sketch.Command

    def color_filler_active(self, color):
        self.filler = fillers.ColorFiller(color)
        self.image_buttons.update_filler(self.filler)

    def elastic_image_filler_active(self, elastic_meta):
        self.filler = fillers.ElasticImageFiller(elastic_meta)
        self.image_buttons.update_filler(self.filler)

    def set_interactive_command(self, command_meta):
        self.interactive_command = command_from_meta(command_meta)

    def save_image(self):
        self.control.winfo_width()
        x = self.position[0]+self.control.winfo_width()
        y = self.position[1]
        x_far = x + self.canvas_size[0]
        y_far = y + self.canvas_size[1]

        image = pyscreenshot.grab((x,y,x_far,y_far))
        file_name = filedialog.asksaveasfilename(initialdir='~/Pictures',
                                                 title='Välj fil',
                                                 filetypes = (("png", "*.png"),("all files","*.*")))
        if file_name:
            image.save(file_name)