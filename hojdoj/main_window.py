import tkinter as tk

import command_terminal
import sketch_control_panel
import sketch
import main_control_panel


class MainWindow(tk.Frame):
    def __init__(self, parent, config, width, height):
        tk.Frame.__init__(self, parent, width=width, height=height)

        output_window_height = 50
        output_window = command_terminal.CommandTerminal(self, locals())
        sketch_height = height-output_window_height
        sketch_control_width = int(width/10)
        main_control_width = int(width/10)
        sketch_width = width - sketch_control_width - main_control_width
        output_window_width = width-sketch_control_width-main_control_width

        main_control_x = sketch_control_width + sketch_width

        sk = sketch.Sketch(self, "sk", config.default_image_template, config, output=output_window)
        sketch_control = sketch_control_panel.SketchControlPanel(self, sk, config)
        main_control = main_control_panel.MainControlPanel(self, parent, sk)
        command_window = command_terminal.CommandTerminal(self, locals())

        sketch_control.place(x=0,y=0, width=sketch_control_width, height=sketch_height)
        sk.place(x=sketch_control_width,y=0, width=sketch_width, height=sketch_height)
        main_control.place(x=main_control_x,y=0, width=main_control_width, height=sketch_height)

        if config["console"]["enabled"]:
            output_window.place(x=sketch_control_width, y=sketch_height, width=output_window_width,
                                height=output_window_height)
