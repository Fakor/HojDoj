
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
