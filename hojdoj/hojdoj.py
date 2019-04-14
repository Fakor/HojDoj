import tkinter as tk

import sys

import main_window
from scrollable_output import ScrollableOutput
from sketch import Sketch
from sketch_control_panel import SketchControlPanel


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

    width = 1680 #   root.winfo_screenwidth()
    height = 1050 #   root.winfo_screenheight()

    root.geometry('{}x{}+{}+{}'.format(int(width/3), int(height/2), 0, int(height/2)))

    main_window = main_window.MainWindow(root, locals())
    main_window.bind('<Return>', lambda eff: enter_pressed(main_window))
    main_window.bind('<Control-c>', lambda eff: quit_hojdoj(root))

    output_window = tk.Toplevel(root)
    output_window.geometry('{}x{}+{}+{}'.format(int(width/3), int(height/2), 0, 0))
    output = ScrollableOutput(output_window)
    output.grid()

    sketch_window = tk.Toplevel(root)
    sketch_window.geometry('{}x{}+{}+{}'.format(int(width * 2 / 3), int(height), int(width/3), 0))
    sk_frame = tk.Frame(sketch_window)
    sk = Sketch(sketch_window, int(width*5/10), height, "sk", image_root, output=output)
    sk_co = SketchControlPanel(sketch_window, sk)
    quit_button = tk.Button(sketch_window, text="Quit", command=lambda: quit_hojdoj(root), anchor=tk.W)

    sk_co.grid(row=0, column=0)
    sk.grid(row=0, column=1)
    quit_button.grid(row=0, column=2)

    root.mainloop()