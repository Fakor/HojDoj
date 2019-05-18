import tkinter as tk

import command_terminal
import scrollable_output
import sketch_control_panel
import sketch
import main_control_panel


class MainWindow(tk.Frame):
    def __init__(self, parent, image_root, width, height):
        tk.Frame.__init__(self, parent, width=width, height=height)
        self.update()
        parent.update()
        output_window = scrollable_output.ScrollableOutput(self)
        sk = sketch.Sketch(self, "sk", image_root, output=output_window)
        sketch_control = sketch_control_panel.SketchControlPanel(self, sk)
        main_control = main_control_panel.MainControlPanel(self, parent)
        command_window = command_terminal.CommandTerminal(self, locals())

        sketch_control.place(x=0,y=0, width=int(width/8), height=int(height*4/5))
        sk.place(x=int(width/8),y=0, width=int(width*5/7), height=int(height*4/5))
        main_control.place(x=int(width*7/8),y=0, width=int(width/7), height=int(height*3/4))
        command_window.place(x=0,y=int(height*4/5), width=int(width/2), height=int(height/5))
        output_window.place(x=int(width/2), y=int(height*4/5), width=int(width / 2), height=int(height / 5))
