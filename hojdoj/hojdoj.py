import tkinter as tk

import main_window
from scrollable_output import ScrollableOutput
from sketch import Sketch


def enter_pressed(console):
    line_private___ = console.get(1.4, tk.END).strip()
    if line_private___[-1] != ":":
        console.shell.runcode(line_private___)


def quit_hojdoj(rt):
    print("Quiting HojDoj!!")
    rt.quit()


if __name__ == '__main__':
    root = tk.Tk()
    root.config(background="red")

    main_window = main_window.MainWindow(root, locals=locals())
    main_window.bind('<Return>', lambda eff: enter_pressed(main_window))
    main_window.bind('<Control-c>', lambda eff: quit_hojdoj(root))

    output_window = tk.Toplevel(root)
    output = ScrollableOutput(output_window)
    output.grid()

    sketch_window = tk.Toplevel(root)
    sk = Sketch(sketch_window, 300, 300, "sk", output=output)
    sk.grid()

    root.mainloop()