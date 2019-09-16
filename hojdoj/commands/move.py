from DTools.base_command import BaseCommand


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.mark_object()
        self.dpos = (0,0)

    def on_move(self, event):
        if self.index is None:
            return
        self.dpos = (event.x - self.init_event.x, event.y - self.init_event.y)
        self.sketch.move_object(self.dpos, index=self.index, intermediate=True)

    def on_release(self, event):
        if self.index is None:
            return
        self.dpos = (event.x - self.init_event.x, event.y - self.init_event.y)
        self.sketch.new_command(self.name,
                                self.dpos,
                                index=self.index)
