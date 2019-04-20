import tkinter as tk

import sys

import main_window
from scrollable_output import ScrollableOutput
from sketch import Sketch
from sketch_control_panel import SketchControlPanel
from configuration import Config
from main_control_panel import MainControlPanel


def enter_pressed(console):
    line_private___ = console.get(1.4, tk.END).strip()
    if line_private___[-1] != ":":
        console.shell.runcode(line_private___)


def quit_hojdoj(rt):
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    print("Quiting HojDoj!!")
    rt.quit()


if __name__ == '__main__':
    image_root = sys.argv[1]

    root = tk.Tk()

    config = Config(root.winfo_screenwidth(), root.winfo_screenheight())

    root.geometry(config.get_command_window_geometry())
    main_window = main_window.MainWindow(root, locals())
    main_window.bind('<Return>', lambda eff: enter_pressed(main_window))

    output_window = tk.Toplevel(root)
    output_window.geometry(config.get_output_window_geometry())
    output = ScrollableOutput(output_window)
    output.grid()

    sketch_window = tk.Toplevel(root)
    sketch_window.geometry(config.get_sketch_window_geometry())
    sk_frame = tk.Frame(sketch_window)
    sk = Sketch(sketch_window, config.sketch_width(), config.height, "sk", image_root, output=output)
    sk_co = SketchControlPanel(sketch_window, sk)
    main_control_panel = MainControlPanel(sketch_window, root)

    sk_co.grid(row=0, column=0)
    sk.grid(row=0, column=1)
    main_control_panel.grid(row=0, column=2)

    root.bind('<<quit_now>>', lambda eff: quit_hojdoj(root))

    root.mainloop()