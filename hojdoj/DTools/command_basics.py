from runpy import run_path


def command_from_meta(command_meta):
    c = run_path(command_meta['path'])
    return c['Command']