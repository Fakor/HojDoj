import tkinter as tk

import interpreter
import main_window


if __name__ == '__main__':
    root = tk.Tk()
    root.config(background="red")
    #interpreter = interpreter.Console(root)
    #interpreter.pack(fill=tk.BOTH,expand=True)
    main_window = main_window.MainWindow(root)

    root.mainloop()