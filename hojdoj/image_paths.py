import PIL


class ImagePaths:
    def __init__(self, image_root):
        self.image_root = image_root

    @property
    def baltazar(self):
        return "{}/baltazar.png".format(self.image_root)

    @property
    def tummen(self):
        return "{}/tummen.png".format(self.image_root)

    @property
    def door1(self):
        return "{}/door1.png".format(self.image_root)

    @property
    def brick_wall(self):
        return "{}/brick_wall.png".format(self.image_root)