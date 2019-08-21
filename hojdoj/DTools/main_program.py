import tkinter as tk


class MainProgram(tk.Frame):

    def __init__(self, parent, config, width, height, output):
        tk.Frame.__init__(self, parent, width=width, height=height)
        self.config = config
        self.output = output

        self.command_index = -1
        self.commands = []

    def undo(self, it=1):
        for i in range(it):
            if self.command_index < 0:
               break
            self.commands[self.command_index].undo()
            self.command_index = self.command_index - 1

    def redo(self, it=1):
        for i in range(it):
            if self.command_index + 1 >= len(self.commands):
                break
            self.command_index = self.command_index + 1
            self.commands[self.command_index].do()

    def add_command(self, command):
        self.command_index += 1
        self.commands = self.commands[:self.command_index]
        self.commands.append(command)
        command.do()
        self.output.print_command(command)