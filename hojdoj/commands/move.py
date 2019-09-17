from DTools.base_command import BaseCommand


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.mark_object()
        self.dpos = (0,0)

    def on_move(self, event):
        if self.index is None:
            return
        self.sketch.move_object(self.delta_position(event), index=self.index, intermediate=True)

    def on_release(self, event):
        if self.index is None:
            return
        self.sketch.new_command(self.name,
                                self.delta_position(event),
                                index=self.index)
