from DTools.command_terminal import command
from sketch import Sketch

from sketch_command import SketchCommand
from move_command import MoveCommand
from delete_command import DeleteCommand
from mark_command import MarkCommand

from DTools.template import Template


class MainWindow:
    def __init__(self, parent, config, width, height):
        self.parent = parent

        self.parent.bind('<Control-c>', self.quit)

        temp = Template(self.parent, Sketch, config, width, height, locals())

        temp.add_control_button(self.quit, text='Quit')
        temp.add_control_button(self.sketch_undo, text='Undo')
        temp.add_control_button(self.sketch_redo, text='Redo')

        temp.place(x=0, y=0, width=width, height=height)

        self.sketch = temp.main

        @command(temp.output_panel)
        def undo(*args, **kwargs):
            self.sketch.undo(*args, **kwargs)

        @command(temp.output_panel)
        def redo(*args, **kwargs):
            self.sketch.redo(*args, **kwargs)

        temp.init_command(SketchCommand)
        temp.init_command(MoveCommand)
        temp.init_command(DeleteCommand)
        temp.init_command(MarkCommand)

    def quit(self, event=None):
        self.parent.event_generate('<<quit_now>>')

    def sketch_undo(self):
        self.sketch.undo_command(it=1)

    def sketch_redo(self):
        self.sketch.redo_command(it=1)
