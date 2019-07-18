import tkinter as tk

import sys

import main_window
import DTools.configuration
import DTools.tk_tools


SCREEN_INDEX = 0


def quit_hojdoj(rt):
    print("Quiting HojDoj!!")
    rt.quit()


if __name__ == '__main__':
    hojdoj_home = sys.argv[1]
    config_path = sys.argv[2]

    config = DTools.configuration.Config(hojdoj_home, config_path)
    root = tk.Tk()

    root.attributes("-fullscreen", True)

    root.geometry(DTools.tk_tools.get_screen_geometry(SCREEN_INDEX))

    main_window = main_window.MainWindow(root, config, *DTools.tk_tools.get_screen_size(SCREEN_INDEX)) #, width=width, height=height)
    main_window.pack()

    root.bind('<<quit_now>>', lambda eff: quit_hojdoj(root))

    root.mainloop()