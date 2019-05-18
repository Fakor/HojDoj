import tkinter as tk

import sys

import main_window
from screeninfo import get_monitors


def quit_hojdoj(rt):
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    print("Quiting HojDoj!!")
    rt.quit()

def get_main_screen_conf():
    main_monitor = get_monitors()[0]
    return main_monitor.width, main_monitor.height, main_monitor.x, main_monitor.y


if __name__ == '__main__':
    image_root = sys.argv[1]

    root = tk.Tk()

    width, height, x, y = get_main_screen_conf()
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    main_window = main_window.MainWindow(root, image_root, width=width, height=height)
    main_window.pack()

    root.bind('<<quit_now>>', lambda eff: quit_hojdoj(root))

    root.mainloop()