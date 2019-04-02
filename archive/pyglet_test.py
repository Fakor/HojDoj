import pyglet


class Interpreter(pyglet.window.Window):
    def __init__(self):
        super(Interpreter, self).__init__(500, 300)
        pyglet.gl.glClearColor(0.5, 0, 0, 1)

        self.doc = pyglet.text.decode_text('Hello world!')

        self.doc.set_style(0, 10, dict(font_name='Times New Roman', font_size=25, color=(255, 255, 255, 255)))
        self.layout= pyglet.text.layout.TextLayout(self.doc, 200, 200, multiline=True, wrap_lines=True)

    def on_draw(self):
        self.clear()
        self.layout.draw()


inter = Interpreter()

pyglet.app.run()