import tkinter as tk

import command_terminal
import scrollable_output
import sketch_control_panel
import sketch
import main_control_panel
import configuration


class MainWindow(tk.Frame):
    def __init__(self, parent, config, width, height):
        tk.Frame.__init__(self, parent, width=width, height=height)

        console_height = int(height/5)
        sketch_height = height-console_height
        sketch_control_width = int(width/10)
        main_control_width = int(width/10)
        sketch_width = width - sketch_control_width - main_control_width
        command_window_width = int(width/2)
        output_window_width = width - command_window_width

        main_control_x = sketch_control_width + sketch_width

        output_window = scrollable_output.ScrollableOutput(self)
        sk = sketch.Sketch(self, "sk", config.default_image_template, output=output_window)
        sketch_control = sketch_control_panel.SketchControlPanel(
            self,
            sk,
            image_templates=config.image_templates,
            image_elastics=config.image_elastics
        )
        main_control = main_control_panel.MainControlPanel(self, parent, sk)
        command_window = command_terminal.CommandTerminal(self, locals())

        sketch_control.place(x=0,y=0, width=sketch_control_width, height=sketch_height)
        sk.place(x=sketch_control_width,y=0, width=sketch_width, height=sketch_height)
        main_control.place(x=main_control_x,y=0, width=main_control_width, height=sketch_height)
        command_window.place(x=0,y=sketch_height, width=command_window_width, height=console_height)
        output_window.place(x=command_window_width, y=sketch_height, width=output_window_width, height=console_height)
