from DTools.tools import value_from_string


class Interpreter:
    def __init__(self, command_table):
        self.command_table = command_table

    def perform_command(self, text):
        pars = text.split(sep='(', maxsplit=1)
        command_str = pars[0]
        tmp = pars[1].strip()

        values = arg_split(tmp)

        args, kwargs = interpret_values(values)
        command = self.get_command(command_str)
        command(*args, **kwargs)

    def get_command(self, command_string):
        return self.command_table[command_string]


def interpret_values(values):
    args = []
    kwargs = {}
    for value in values:
        if '=' in value:
            tmp = value.split('=')
            kwargs[tmp[0].strip()] = value_from_string(tmp[1])
        else:
            args.append(value_from_string(value))

    return args, kwargs


def arg_split(text):
    args = []
    i = 0
    arg_start = 0
    while i < len(text):
        if text[i] == ',' or text[i] == ')':
            if arg_start != i:
                args.append(text[arg_start:i].strip())
            arg_start = i + 1
        elif text[i] == '(':
            i = text[i:].find(')') + i
        elif text[i] == '[':
            i = text[i:].find(']') + i

        i += 1
    return args
