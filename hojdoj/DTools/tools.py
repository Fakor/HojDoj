import numpy as np
import PIL
from PIL import ImageTk


def value_to_string(value):
    if isinstance(value, str):
        return '"{}"'.format(value)
    return str(value)


def value_from_string(text):
    txt_tmp = text.strip(" \"\'")
    if txt_tmp[0] == '(':
        txt_tmp = txt_tmp.strip('()')
        return tuple((value_from_string(el) for el in txt_tmp.split(',')))
    try:
        return int(txt_tmp)
    except ValueError:
        try:
            return float(txt_tmp)
        except ValueError:
            return txt_tmp


def sum_points(*points):
    return [sum(el) for el in zip(*points)]


def image_replace_white(image, new):
    image = image.convert('RGBA')
    data = np.array(image)
    red, green, blue, alpha = data.T
    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][white_areas.T] = new
    return PIL.Image.fromarray(data)


def image_replace_elastic(image, elastic_image, vertical=True):
    image = image.convert('RGBA')
    data = np.array(image)

    if vertical:
        el_back = elastic_background_vertical(elastic_image, (data.shape[1], data.shape[0]), as_photo_image=False)
    else:
        el_back = elastic_background_horizontal(elastic_image, (data.shape[1], data.shape[0]), as_photo_image=False)
    elastic_data = np.array(el_back)
    red, green, blue, alpha = data.T
    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][white_areas.T] = elastic_data[..., :3][white_areas.T]
    return PIL.Image.fromarray(data)


def elastic_background_horizontal(elastic_image, size, as_photo_image=True):
    data = np.array(elastic_image)
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

    if as_photo_image:
        return ImageTk.PhotoImage(img)
    return img


def elastic_background_vertical(elastic_image, size, as_photo_image=True):
    data = np.array(elastic_image)
    rows, cols, K = data.shape

    new_cols, new_rows = size

    new_data = np.zeros((new_rows, new_cols, K), dtype=np.uint8)

    current_row = 0
    current_col = 0

    org_row = 0
    while True:
        M = np.min((rows-org_row, new_rows - current_row))
        N = np.min((new_cols - current_col, cols))
        new_data[current_row:current_row+M,current_col:current_col+N,:] = data[org_row:org_row+M,0:N,:]
        if current_row+M == new_rows:
            if current_col + N == new_cols:
                break
            current_row = 0
            current_col = current_col + N
        else:
            current_row = current_row + M
        org_row = org_row + M
        if org_row == rows:
            org_row = 0
    img = PIL.Image.fromarray(new_data)

    if as_photo_image:
        return PIL.ImageTk.PhotoImage(img)
    return img
