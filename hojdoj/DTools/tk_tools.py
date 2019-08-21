from DTools.screeninfo import get_monitors


def get_screen_geometry(index):
    m = get_monitors()[index]
    return '{}x{}+{}+{}'.format(m.width, m.height, m.x, m.y)


def get_screen_size(index):
    m = get_monitors()[index]
    return m.width, m.height


def get_screen_position(index):
    m = get_monitors()[index]
    return m.x, m.y


def color_to_tk(color):
    return '#{}{}{}'.format(*["{0:#0{1}x}".format(el, 4).replace("0x", "") for el in color])
