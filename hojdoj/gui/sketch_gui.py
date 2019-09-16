import tkinter as tk
from PIL import ImageTk
from tkinter import filedialog
import pyscreenshot

from DTools.tk_tools import color_to_tk
from DTools.button_grid import ButtonGrid
from DTools import fillers
from DTools.command_basics import command_from_meta
from logic.sketch_logic import SketchLogic
from DTools.tools import sum_points


DRAW_COMMAND='draw'


class SketchGui(tk.Frame):
    COLUMNS = 4

    def __init__(self, parent, config, position, size):
        width, height = size
        tk.Frame.__init__(self, parent, width=width, height=height)

        self.logic = SketchLogic(config['image_templates'], config['fillers'])
        self.images = {}

        bg_color = color_to_tk(config.get_value('background_color'))
        self.canvas = tk.Canvas(self, borderwidth=4, relief=tk.GROOVE, background=bg_color)

        self.parent = parent
        self.position = position
        self.config = config

        self.objects = {}
        self.marked_object = None

        self.current_image = self.config.get_value('default_image')

        self.canvas.bind("<Button-1>", self.on_button1_press)
        self.canvas.bind("<Button-3>", self.on_button2_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<B3-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<ButtonRelease-3>", self.on_button_release)

        self.filler = config['default_color']

        canvas_width = int(width*0.9)
        canvas_height = height

        control_width = width-canvas_width
        control_height = canvas_height

        self.canvas.place(x=control_width, y=0, width=canvas_width, height=canvas_height)

        self.current_command = None
        self.interactive_command_name = DRAW_COMMAND

        self.control = tk.Frame(self)
        self.control.place(x=0, y=0, width=control_width, height=control_height)

        self.B_WIDTH = int(0.87*control_width/SketchGui.COLUMNS)
        self.B_HEIGHT = self.B_WIDTH

        self.canvas_position = width, 0
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
                                          self.logic.get_filler(color),
                                          self.color_filler_active,
                                          color)
        self.color_buttons.grid(row=2)

        self.elastic_buttons = ButtonGrid(self.control, SketchGui.COLUMNS, self.B_WIDTH, self.B_HEIGHT, header='Elastisk', background='white')
        for elastic in self.config['fillers'].keys():
            self.elastic_buttons.add_button(config['color_button_image_path'],
                                            self.logic.get_filler(elastic),
                                            self.elastic_image_filler_active,
                                            elastic)

        self.elastic_buttons.grid(row=3)
        self.start_motion_cycle()

    def new_command(self, command_name, *args, **kwargs):
        self.parent.new_command(command_name, *args, **kwargs)

    def draw_object(self, *args, **kwargs):
        return self.logic.draw_object(self.draw_object_callback, *args, **kwargs)

    def draw_object_callback(self, index, position, logic_image):
        self._delete(index)
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

    def mark_object_by_index(self, index):
        return self.logic.mark_object_by_index(self.mark_object_callback, index)

    def mark_object_callback(self, index):
        self.marked_object = index
        return self.marked_object

    def rotate_object(self, *args, **kwargs):
        self.logic.rotate_object(self.rotate_object_callback, *args, **kwargs)

    def rotate_object_callback(self, index, rotation, logic_image):
        self._delete(index)
        new_image = ImageTk.PhotoImage(logic_image.image)
        self.objects[index] = self.canvas.create_image(*logic_image.position, image=new_image)
        self.images[index] = new_image

    def resize_object(self, *args, **kwargs):
        self.logic.resize_object(self.resize_object_callback, *args, **kwargs)

    def resize_object_callback(self, index, size, logic_image):
        self._delete(index)
        if not any([el<=0 for el in size]):
            new_image = ImageTk.PhotoImage(logic_image.image)
            self.objects[index] = self.canvas.create_image(*logic_image.position, image=new_image)
            self.images[index] = new_image

    def delete_object(self, index=None):
        self.logic.delete_object(self.delete_object_callback, index)

    def delete_object_callback(self, index):
        if self._delete(index):
            self.images.pop(index)

    def set_velocity(self, *args, **kwargs):
        self.logic.set_velocity(self.set_velocity_callback, *args, **kwargs)

    def set_velocity_callback(self, index, velocity):
        pass

    def set_acceleration(self, *args, **kwargs):
        self.logic.set_acceleration(self.set_acceleration_callback, *args, **kwargs)

    def set_acceleration_callback(self, index, acceleration):
        pass

    def set_motion(self, *args, **kwargs):
        self.logic.set_motion(*args, **kwargs)

    def set_gravity(self, gravity):
        self.logic.gravity = gravity

    def get_command_table(self):
        return {
            'draw': self.draw_object,
            'move': self.move_object,
            'rotate': self.rotate_object,
            'resize': self.resize_object,
            'mark': self.mark_object_by_index,
            'delete': self.delete_object,
            'vel': self.set_velocity,
            'acc': self.set_acceleration,
            'motion': self.set_motion,
            'gravity': self.set_gravity,
            'save': self.save_image
        }

    def on_button1_press(self, event):
        command = command_from_meta(self.config['commands'][self.interactive_command_name])
        self.current_command = command(self, event, self.interactive_command_name)

    def on_button2_press(self, event):
        command = command_from_meta(self.config['commands'][self.interactive_command_name])
        self.current_command = command(self, event, self.interactive_command_name, button2=True)

    def on_move_press(self, event):
        self.current_command.on_move(event)

    def on_button_release(self, event):
        self.current_command.on_release(event)

    def set_interactive_command(self, command_name):
        self.interactive_command_name = command_name

    def image_tool_active(self, image_name):
        self.current_image = image_name
        self.interactive_command_name = DRAW_COMMAND

    def color_filler_active(self, color):
        self.filler = tuple(color)
        self.image_buttons.update_filler(self.logic.get_filler(color))

    def elastic_image_filler_active(self, name):
        self.filler = name
        self.image_buttons.update_filler(self.logic.get_filler(name))

    def get_image_path(self, image_name):
        return self.config['image_templates'][image_name]

    def get_object_position(self, index):
        return self.logic.object_position(index)

    def get_object_size(self, index):
        return self.logic.object_size(index)

    def start_motion_cycle(self):
        updates = self.logic.step()
        for index, position in updates:
            try:
                self.canvas.coords(self.objects[index], *position)
            except KeyError:
                # Need to catch this exception since there might be a
                # race condition problem were the logic sends back updated
                # indexes that have not yet been registered here.
                pass
        self.after(self.config['step_time'], self.start_motion_cycle)

    def save_image(self):
        size = sum_points(self.canvas_position, self.canvas_size)
        image = pyscreenshot.grab((*self.canvas_position, *size))
        file_name = filedialog.asksaveasfilename(initialdir=self.config['save_location'],
                                                 title='Välj fil',
                                                 filetypes = (("png", "*.png"),("all files","*.*")))
        if file_name:
            image.save(file_name)

    def _delete(self, index):
        if index in self.objects:
            self.canvas.delete(self.objects[index])
            return True
        return False
