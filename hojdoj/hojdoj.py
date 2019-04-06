import tkinter as tk

import main_window


if __name__ == '__main__':
    root = tk.Tk()
    root.config(background="red")
    main_window = main_window.MainWindow(root)

    root.mainloop()