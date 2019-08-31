
def draw_callback(index, position, image):
    return index, position


def move_callback(index, position):
    return index, position


def mark_callback(index):
    return index


def delete_callback(index):
    return index


def rotate_callback(index, image):
    return index, image.rotation