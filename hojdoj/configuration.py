import json
import pathlib
import os

GEOMETRY='{}x{}+{}+{}'


class Config:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.custom_config_path = os.path.join(pathlib.Path.home(), ".hojdoj_config.json")

        if os.path.isfile(self.custom_config_path):
            with open(self.custom_config_path) as f:
                self.custom_config = json.load(f)
        else:
            self.custom_config = {}

    def get_command_window_geometry(self):
        conf = self.custom_config.get("command", {})
        x = conf.get('x', 0)
        y = conf.get('y', int(self.height/2))
        width = conf.get("width", int(self.width / 3))
        height = conf.get("height", int(self.height / 2))
        return GEOMETRY.format(width, height, x, y)

    def get_output_window_geometry(self):
        conf = self.custom_config.get("output", {})
        x = conf.get('x', 0)
        y = conf.get('y', 0)
        width = conf.get("width", int(self.width / 3))
        height = conf.get("height", int(self.height / 2))
        return GEOMETRY.format(width, height, x, y)

    def get_sketch_window_geometry(self):
        conf = self.custom_config.get("sketch", {})
        x = conf.get('x', int(self.width/3))
        y = conf.get('y', 0)
        width = conf.get("width", int(self.width * 2/ 3))
        height = conf.get("height", int(self.height))
        return GEOMETRY.format(width, height, x, y)
