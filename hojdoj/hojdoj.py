import tkinter as tk

import sys

import main_window
from scrollable_output import ScrollableOutput
from sketch import Sketch
from sketch_control_panel import SketchControlPanel
from configuration import Config


def enter_pressed(console):
    line_private___ = console.get(1.4, tk.END).strip()
    if line_private___[-1] != ":":
        console.shell.runcode(line_private___)


def quit_hojdoj(rt):
    print("Quiting HojDoj!!")
    rt.quit()


if __name__ == '__main__':
    image_root = sys.argv[1]

    root = tk.Tk()

    config = Config(root.winfo_screenwidth(), root.winfo_screenheight())

    root.geometry(config.get_command_window_geometry())
    main_window = main_window.MainWindow(root, locals())
    main_window.bind('<Return>', lambda eff: enter_pressed(main_window))
    main_window.bind('<Control-c>', lambda eff: quit_hojdoj(root))

    output_window = tk.Toplevel(root)
    output_window.geometry(config.get_output_window_geometry())
    output = ScrollableOutput(output_window)
    output.grid()

    sketch_window = tk.Toplevel(root)
    sketch_window.geometry(config.get_sketch_window_geometry())
    sk_frame = tk.Frame(sketch_window)
    sk = Sketch(sketch_window, int(config.width*5/12), config.height, "sk", image_root, output=output)
    sk_co = SketchControlPanel(sketch_window, sk)
    quit_button = tk.Button(sketch_window, text="Quit", command=lambda: quit_hojdoj(root), anchor=tk.W)

    sk_co.grid(row=0, column=0)
    sk.grid(row=0, column=1)
    quit_button.grid(row=0, column=2)

    root.mainloop()