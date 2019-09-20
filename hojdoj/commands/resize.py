from DTools.base_command import BaseCommand


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.mark_object()
        if self.index is None:
            return
        pos = self.logic.object_position(self.index)
        self.mark_on_right = pos[0] < self.init_event.x
        self.mark_on_up = pos[1] < self.init_event.y

    def on_move(self, event):
        if self.index is None:
            return
        dpos = self.get_dpos(event.x, event.y)
        self.logic.resize_object(dpos, index=self.index, intermediate=True)

    def on_release(self, event):
        if self.index is None:
            return
        dpos = self.get_dpos(event.x, event.y)
        self.perform_command(self.name,
                             dpos,
                             index=self.index)

    def get_dpos(self, x, y):
        dx = 2*(self.init_event.x - x)
        if self.mark_on_right:
            dx *= -1
        dy = 2 * (self.init_event.y - y)
        if self.mark_on_up:
            dy *= -1
        return dx, dy
