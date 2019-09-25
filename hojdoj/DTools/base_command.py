from DTools.tools import value_to_string


class BaseCommand:
    def __init__(self, logic, event, command_name, button2=False):
        self.name = command_name
        self.logic = logic
        self.init_event = event
        self.button2 = button2
        self.index = None

    def on_move(self, event):
        raise NotImplemented

    def on_release(self, event):
        raise NotImplemented

    def mark_object(self):
        self.logic.mark_object((self.init_event.x, self.init_event.y))
        self.index = self.logic.marked_object_index
        return self.index is not None

    def delta_position(self, event):
        return event.x - self.init_event.x, event.y - self.init_event.y

    def perform_command(self, command_name, *args, **kwargs):
        text = "{}(".format(command_name)

        args_text = [value_to_string(arg) for arg in args]
        kwargs_text =['{}={}'.format(str(key),value_to_string(value)) for key, value in kwargs.items() if value is not None]
        text = text + ', '.join(args_text  + kwargs_text) + ")"

        self.logic.perform_command(text)
