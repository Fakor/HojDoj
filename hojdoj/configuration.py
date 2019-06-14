import json

GEOMETRY='{}x{}+{}+{}'


class Config:
    def __init__(self, hojdoj_home, config_path):
        with open(config_path) as f:
            text = f.read()
        text = text.replace("$HOJDOJ_HOME", hojdoj_home)
        self.conf = json.loads(text)

    @property
    def default_image_template(self):
        return self.conf["default_image_template"]

    @property
    def image_templates(self):
        return self.conf["image_templates"]

    @property
    def image_elastics(self):
        return self.conf["image_elastics"]

    @property
    def sketch_colors(self):
        return [tuple(el) for el in self.conf["sketch_colors"]]

    @property
    def default_color(self):
        return self.conf["default_color"]

    def __getitem__(self, item):
        return self.conf[item]

    def get_image_meta(self, name):
        for m in self.conf['image_templates']:
            if m['name'] == name:
                return m
        raise AttributeError("Image with name {} not found!", name)

    def get_elastic_meta(self, name):
        for m in self.conf['image_elastics']:
            if m['name'] == name:
                return m
        raise AttributeError("Image with name {} not found!", name)