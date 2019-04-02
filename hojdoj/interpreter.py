import tkinter as tk
import subprocess
import queue
import os
from threading import Thread


class Console(tk.Frame):
    def __init__(self,parent=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.create_widgets()

        # get the path to the console.py file assuming it is in the same folder
        console_path = os.path.join(os.path.dirname(__file__),"console.py")
        # open the console.py file (replace the path to python with the correct one for your system)
        # e.g. it might be "C:\\Python35\\python"
        self.p = subprocess.Popen(["python3",console_path],
                                  stdout=subprocess.PIPE,
                                  stdin=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

        # make queues for keeping stdout and stderr whilst it is transferred between threads
        self.outQueue = queue.Queue()
        self.errQueue = queue.Queue()

        # keep track of where any line that is submitted starts
        self.line_start = 0

        # make the enter key call the self.enter function
        self.ttyText.bind("<Return>",self.enter)

        # a daemon to keep track of the threads so they can stop running
        self.alive = True
        # start the functions that get stdout and stderr in separate threads
        Thread(target=self.read_from_proccess_out).start()
        Thread(target=self.read_from_process_err).start()

        # start the write loop in the main thread
        self.write_loop()
        self.pack(fill=tk.BOTH, expand=True)

    def destroy(self):
        """
        This is the function that is automatically called when the widget is destroyed.
        """
        self.alive=False
        # write exit() to the console in order to stop it running
        self.p.stdin.write("exit()\n".encode())
        self.p.stdin.flush()
        # call the destroy methods to properly destroy widgets
        self.ttyText.destroy()
        tk.Frame.destroy(self)

    def enter(self,e):
        """
        The <Return> key press handler
        """
        string = self.ttyText.get(1.0, tk.END)[self.line_start:]
        self.line_start+=len(string)
        self.p.stdin.write(string.encode())
        self.p.stdin.flush()

    def read_from_proccess_out(self):
        """
        To be executed in a separate thread to make read non-blocking
        """
        while self.alive:
            data = self.p.stdout.raw.read(1024).decode()
            self.outQueue.put(data)

    def read_from_process_err(self):
        """
        To be executed in a separate thread to make read non-blocking
        """
        while self.alive:
            data = self.p.stderr.raw.read(1024).decode()
            self.errQueue.put(data)

    def write_loop(self):
        """
        Used to write data from stdout and stderr to the Text widget
        """
        # if there is anything to write from stdout or stderr, then write it
        if not self.errQueue.empty():
            self.write(self.errQueue.get())
        if not self.outQueue.empty():
            self.write(self.outQueue.get())

        # run this method again after 10ms
        if self.alive:
            self.after(10, self.write_loop)

    def write(self,string):
        self.ttyText.insert(tk.END, string)
        self.ttyText.see(tk.END)
        self.line_start+=len(string)

    def create_widgets(self):
        self.ttyText = tk.Text(self, wrap=tk.WORD)
        self.ttyText.pack(fill=tk.BOTH,expand=True)


