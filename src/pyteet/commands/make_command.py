from pyteet import camel_to_snake, render_template

import argparse
from pathlib import Path

NAME = 'make:command'
DESC = 'Create a new command'

def run(args):
    parser = argparse.ArgumentParser(
            description=DESC,
            usage=NAME)
    parser.add_argument('name')
    parsed = parser.parse_args(args)
    proj_root = Path().cwd()
    name = camel_to_snake(parsed.name)
    path = proj_root / 'commands' / f'{name}.py'
    if path.exists():
        raise ValueError(f'{path} already exists.')
    with open(path.as_posix(), 'w') as w:
        w.write(render_template('command.py', name=name))
    print(f'created: {path.as_posix()}')

