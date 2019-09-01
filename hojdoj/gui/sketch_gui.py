import tkinter as tk
from PIL import ImageTk

from DTools.tk_tools import color_to_tk
from DTools.button_grid import ButtonGrid
from DTools import fillers
from commands import sketch
from DTools.command_basics import command_from_meta
from logic.sketch_logic import SketchLogic


class SketchGui(tk.Frame):
    COLUMNS = 4

    def __init__(self, parent, config, position, size):
        width, height = size
        tk.Frame.__init__(self, parent, width=width, height=height)

        self.logic = SketchLogic(config['image_templates'])
        self.images = {}

        bg_color = color_to_tk(config.get_value('background_color'))
        self.canvas = tk.Canvas(self, borderwidth=4, relief=tk.GROOVE, background=bg_color)

        self.parent = parent
        self.position = position
        self.config = config

        self.objects = {}
        self.marked_object = None

        self.current_image = self.config.get_value('default_image')

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.parent.bind('<Control-z>', self._undo)
        self.parent.bind('<Control-y>', self._redo)

        self.filler = (255, 255, 255)

        canvas_width = int(width*0.87)
        canvas_height = height

        control_width = width-canvas_width
        control_height = canvas_height

        self.canvas.place(x=control_width, y=0, width=canvas_width, height=canvas_height)

        self.current_command = None
        self.interactive_command_name = "draw"

        self.control = tk.Frame(self)
        self.control.place(x=0, y=0, width=control_width, height=control_height)

        self.B_WIDTH = int(0.94*control_width/SketchGui.COLUMNS)
        self.B_HEIGHT = self.B_WIDTH

        x, y = size
        self.canvas_position = x, 0
        self.canvas_size = canvas_width, canvas_height

        self.command_buttons = ButtonGrid(self.control, SketchGui.COLUMNS, self.B_WIDTH, self.B_HEIGHT, header="Commands", background='white')
        for name, command_meta in config['commands'].items():
            if 'image' in command_meta:
                self.command_buttons.add_button(command_meta['image'],
                                                fillers.NoFiller(),
                                                self.set_interactive_command,
                                                name)
        self.command_buttons.grid(row=0)

        self.image_buttons = ButtonGrid(self.control, SketchGui.COLUMNS, self.B_WIDTH, self.B_HEIGHT, header="Bilder", background='white')
        for name, path in config['image_templates'].items():
            self.image_buttons.add_button(path,
                                          self.logic.get_filler(config['default_color']),
                                          self.image_tool_active,
                                          name)
        self.image_buttons.grid(row=1)

        self.color_buttons = ButtonGrid(self.control, SketchGui.COLUMNS, self.B_WIDTH, self.B_HEIGHT, header="Färger", background='white')
        for color in config['sketch_colors']:
            self.color_buttons.add_button(config['color_button_image_path'],
                                          fillers.ColorFiller(color),
                                          self.color_filler_active,
                                          color)
        self.color_buttons.grid(row=2)

        # self.elastic_buttons = ButtonGrid(self.control, SketchGui.COLUMNS, self.B_WIDTH, self.B_HEIGHT, header='Elastisk', background='white')
        # for elastic in self.config['image_elastics']:
        #     self.elastic_buttons.add_button(config['color_button_image_path'],
        #                                     fillers.ElasticImageFiller(elastic),
        #                                     self.elastic_image_filler_active,
        #                                     elastic)
        #
        # self.elastic_buttons.grid(row=3)

    def new_command(self, command_name, *args, **kwargs):
        self.parent.new_command(command_name, *args, **kwargs)

    def draw_object(self, *args, **kwargs):
        return self.logic.draw_object(self.draw_object_callback, *args, **kwargs)

    def draw_object_callback(self, index, position, logic_image):
        if index in self.objects:
            self.canvas.delete(self.objects[index])
        if logic_image.have_size():
            new_image = ImageTk.PhotoImage(logic_image.image)
            self.objects[index] = self.canvas.create_image(*position, image=new_image)
            self.images[index] = new_image
        return index

    def move_object(self, *args, **kwargs):
        self.logic.move_object(self.move_object_callback, *args, **kwargs)

    def move_object_callback(self, index, position):
        self.canvas.coords(self.objects[index], *position)

    def mark_object(self, position):
        return self.logic.mark_object(self.mark_object_callback, position)

    def mark_object_callback(self, index):
        self.marked_object = index
        return self.marked_object

    def rotate_object(self, *args, **kwargs):
        self.logic.rotate_object(self.rotate_object_callback, *args, **kwargs)

    def rotate_object_callback(self, index, rotation, logic_image):
        self.canvas.delete(self.objects[index])
        new_image = ImageTk.PhotoImage(logic_image.image)
        self.objects[index] = self.canvas.create_image(*logic_image.position, image=new_image)
        self.images[index] = new_image

    def resize_object(self, *args, **kwargs):
        self.logic.resize_object(self.resize_object_callback, *args, **kwargs)

    def resize_object_callback(self, index, size, logic_image):
        self.canvas.delete(self.objects[index])
        if not any([el<=0 for el in size]):
            new_image = ImageTk.PhotoImage(logic_image.image)
            self.objects[index] = self.canvas.create_image(*logic_image.position, image=new_image)
            self.images[index] = new_image

    def delete_object(self, index):
        self.logic.delete_object(self.delete_object_callback, index)

    def delete_object_callback(self, index):
        self.canvas.delete(self.objects.pop(index))
        self.images.pop(index)

    def get_command_table(self):
        return {
            'draw': self.draw_object,
            'move': self.move_object,
            'rotate': self.rotate_object,
            'resize': self.resize_object,
            'delete': self.delete_object
        }

    def on_button_press(self, event):
        command = command_from_meta(self.config['commands'][self.interactive_command_name])
        self.current_command = command(self, event, self.interactive_command_name)

    def on_move_press(self, event):
        self.current_command.on_move(event)

    def on_button_release(self, event):
        self.current_command.on_release(event)

    def set_interactive_command(self, command_name):
        self.interactive_command_name = command_name

    def image_tool_active(self, image_meta):
        self.current_image = image_meta
        self.interactive_command = sketch.Command

    def color_filler_active(self, color):
        self.filler = tuple(color)
        self.image_buttons.update_filler(fillers.ColorFiller(color))

    def elastic_image_filler_active(self, elastic_meta):
        self.filler = fillers.ElasticImageFiller(elastic_meta)
        self.image_buttons.update_filler(self.filler)

    def get_image_path(self, image_name):
        return self.config['image_templates'][image_name]

    def get_object_position(self, index):
        return self.logic.object_position(index)

    def get_object_size(self, index):
        return self.logic.object_size(index)

    def _undo(self, event):
        self.undo_command()

    def _redo(self, event):
        self.redo_command()