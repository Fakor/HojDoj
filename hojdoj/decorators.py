

def call_syntax(func):
    def wrapper(self, *args, **kwargs):
        text = "{}.{}(".format(self.name, func.__name__)
        if len(args) > 0:
            text = text + str(args[0])
            for arg in args[1:]:
                text = text + ',' + str(arg)
        text = text + ")"
        self.output.add_row(text)
        return func(self, *args, **kwargs)
    return wrapper
