import numpy as np
import PIL


class Colors:
    RED = {'RGB': (255, 0.0, 0.0), 'tk': '#ff0000'}
    GREEN = {'RGB': (0.0, 255, 0.0), 'tk': '#00ff00'}
    BLUE = {'RGB': (0.0, 0.0, 255), 'tk': '#0000ff'}
    WHITE = {'RGB': (255, 255, 255), 'tk': '#ffffff'}
    BLACK = {'RGB': (0, 0, 0), 'tk': '#000000'}


def base_call(func):
    def wrapper(self, *args, **kwargs):
        text = "{}.{}(".format(self.name, func.__name__)
        if len(args) > 0:
            text = text + value_to_string(args[0])
            for arg in args[1:]:
                text = text + ',' + value_to_string(arg)
        if len(kwargs) > 0:
            first_done = False
            for key, value in kwargs.items():
                if not first_done and len(args) == 0:
                    text = text + str(key) + '=' + value_to_string(value)
                else:
                    text = text + ',' + str(key) + '=' + value_to_string(value)
        text = text + ")"
        self.output.add_command(text)
        return func(self, *args, **kwargs)
    return wrapper


def object_call(base_func):
    def object_call_wrapper(func):
        def wrapper(self, *args, **kwargs):
            new_id = base_func(self, *args, **kwargs)
            self.objects.append({"id": new_id,
                                 "command": base_func,
                                 "args":args,
                                 "kwargs": kwargs}
            )
            text = "{}.{}(".format(self.name, func.__name__)
            if len(args) > 0:
                text = text + value_to_string(args[0])
                for arg in args[1:]:
                    text = text + ',' + value_to_string(arg)
            if len(kwargs) > 0:
                first_done = False
                for key, value in kwargs.items():
                    if not first_done and len(args) == 0:
                        text = text + str(key) + '=' + value_to_string(value)
                    else:
                        text = text + ',' + str(key) + '=' + value_to_string(value)
            text = text + ")"
            self.output.add_command(text)
            return func(self, *args, **kwargs)
        return wrapper
    return object_call_wrapper


def value_to_string(value):
    if isinstance(value, str):
        return '"{}"'.format(value)
    return str(value)


def image_replace_white(image, new):
    image = image.convert('RGBA')
    data = np.array(image)
    red, green, blue, alpha = data.T
    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][white_areas.T] = new
    return PIL.Image.fromarray(data)


def elastic_background(path, size):
    img = PIL.Image.open(path)
    data = np.array(img)
    rows, cols, K = data.shape

    new_cols, new_rows = size

    new_data = np.zeros((new_rows, new_cols, K), dtype=np.uint8)

    current_row = 0
    current_col = 0

    org_col = 0
    while True:
        M = np.min((rows, new_rows - current_row))
        N = np.min((new_cols - current_col, cols-org_col))
        new_data[current_row:current_row+M,current_col:current_col+N,:] = data[0:M,org_col:org_col+N,:]
        if current_col+N == new_cols:
            if current_row + M == new_rows:
                break
            current_col = 0
            current_row = current_row + M
        else:
            current_col = current_col + N
        org_col = org_col + N
        if org_col == cols:
            org_col = 0
    img = PIL.Image.fromarray(new_data)
    return PIL.ImageTk.PhotoImage(img)