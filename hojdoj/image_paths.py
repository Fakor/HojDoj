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