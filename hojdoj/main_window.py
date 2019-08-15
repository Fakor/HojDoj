from DTools.command_terminal import command
from sketch import Sketch

from DTools.template import Template


class MainWindow:
    def __init__(self, parent, config, position, size):
        self.parent = parent
        self.parent.bind('<Control-c>', self.quit)

        width, height = size

        temp = Template(self.parent, Sketch, config, position, size, locals())

        temp.add_control_button(self.quit, text='Quit')
        temp.add_control_button(self.sketch_undo, text='Undo')
        temp.add_control_button(self.sketch_redo, text='Redo')
        temp.add_control_button(self.sketch_save_image, text='Save')

        temp.place(x=0, y=0, width=width, height=height)

        self.sketch = temp.main

        @command(temp.output_panel)
        def undo(*args, **kwargs):
            self.sketch.undo(*args, **kwargs)

        @command(temp.output_panel)
        def redo(*args, **kwargs):
            self.sketch.redo(*args, **kwargs)

        temp.init_commands(config['commands'])

    def quit(self, event=None):
        self.parent.event_generate('<<quit_now>>')

    def sketch_undo(self):
        self.sketch.undo(it=1)

    def sketch_redo(self):
        self.sketch.redo(it=1)

    def sketch_save_image(self):
        self.sketch.save_image()