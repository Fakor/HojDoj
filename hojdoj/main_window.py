from DTools.command_terminal import command
from sketch import Sketch

from commands import SketchImageCommand, MoveImageCommand, DeleteImageCommand, MarkImageCommand
from DTools.template import Template

import sketch_interactive
import delete_interactive
import mark_interactive
import move_interactive


class MainWindow:
    def __init__(self, parent, config, width, height):
        self.parent = parent

        self.parent.bind('<Control-c>', self.quit)

        temp = Template(self.parent, Sketch, config, width, height, locals())

        temp.add_control_button(self.quit, text='Quit')
        temp.add_control_button(self.sketch_undo, text='Undo')
        temp.add_control_button(self.sketch_redo, text='Redo')
        temp.add_control_button(self.interactive_sketch, text='Sketch')
        temp.add_control_button(self.interactive_delete, text='Delete')
        temp.add_control_button(self.interactive_mark, text='Mark')
        temp.add_control_button(self.interactive_move, text='Move')

        temp.place(x=0, y=0, width=width, height=height)

        self.sketch = temp.main

        @command(temp.output_panel)
        def move(*args, **kwargs):
            self.sketch.add_command(MoveImageCommand, *args, **kwargs)

        @command(temp.output_panel)
        def sketch(*args, **kwargs):
            self.sketch.add_command(SketchImageCommand, *args, **kwargs)

        @command(temp.output_panel)
        def delete(*args, **kwargs):
            self.sketch.add_command(DeleteImageCommand, *args, **kwargs)

        @command(temp.output_panel)
        def mark(*args, **kwargs):
            self.sketch.add_command(MarkImageCommand, *args, **kwargs)

        @command(temp.output_panel)
        def undo(*args, **kwargs):
            self.sketch.undo(*args, **kwargs)

        @command(temp.output_panel)
        def redo(*args, **kwargs):
            self.sketch.redo(*args, **kwargs)

        self.sketch.set_command_functions(move, sketch, delete, mark, undo, redo)

        temp.update_locals(locals())

    def quit(self, event=None):
        self.parent.event_generate('<<quit_now>>')

    def sketch_undo(self):
        self.sketch.undo_command(it=1)

    def sketch_redo(self):
        self.sketch.redo_command(it=1)

    def interactive_sketch(self):
        self.sketch.interactive_command = sketch_interactive.SketchInteractive

    def interactive_delete(self):
        self.sketch.interactive_command = delete_interactive.DeleteInteractive

    def interactive_mark(self):
        self.sketch.interactive_command = mark_interactive.MarkInteractive

    def interactive_move(self):
        self.sketch.interactive_command = move_interactive.MoveInteractive