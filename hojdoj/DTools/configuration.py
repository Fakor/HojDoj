import json


class Config:
    def __init__(self, proj_home, config_path):
        with open(config_path) as f:
            text = f.read()
        text = text.replace("$PROJ_HOME", proj_home)
        self.conf = json.loads(text)

    def get_value(self, *args):
        value = self.conf[args[0]]
        for arg in args[1:]:
            value = value[arg]
        return value

    def get_first_value(self, *args, **kwargs):
        value = self.get_value(*args)
        for item in value:
            for key, v in kwargs.items():
                if item[key] != v:
                    break
                return item
        raise AttributeError()

    def __getitem__(self, item):
        return self.conf[item]
