

def call_syntax(func):
    def wrapper(self, *args, **kwargs):
        text = "{}.{}(".format(self.name, func.__name__)
        text = text + ")"
        self.output.add_row(text)
        return func(self, *args, **kwargs)
    return wrapper
