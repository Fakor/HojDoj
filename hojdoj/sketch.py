import tkinter as tk


class Sketch(tk.Canvas):
    def __init__(self, parent, width, height):
        tk.Canvas.__init__(self, parent, width=width, height=height)
        self._layers = []
        self.pack()
        # draw a circle on layer 1:
        self.add_to_layer(1, self.create_oval, (100,10,30,40), outline="red")
        # draw a square on layer 2:
        self.add_to_layer(2, self.create_rectangle, (10,10,50,60), fill="blue")
        print(self._layers)

    def add_to_layer(self, layer, command, cords, **kwargs):
        layer_tag = "layer %s" % layer
        if layer_tag not in self._layers: self._layers.append(layer_tag)
        tags = kwargs.setdefault("tags", [])
        tags.append(layer_tag)
        item_id = command(cords, **kwargs)
        self._adjust_layers()
        return item_id

    def _adjust_layers(self):
        for layer in sorted(self._layers):
            self.lift(layer)