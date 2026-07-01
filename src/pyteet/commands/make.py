from pyteet import camel_to_snake, render_template

import argparse
import importlib
from pathlib import Path

NAME = 'make'
DESC = 'Create a new resource'

def run(args):
    parser = argparse.ArgumentParser(
            description=DESC,
            usage=NAME)
    parser.add_argument(
            'resource',
            help='command, controller, migration, model',
            type=str)
    parser.add_argument(
            'name',
            help='resource name',
            type=str)
    parsed = parser.parse_args(args)
    module = importlib.import_module(__name__)
    task = getattr(module, f'_{parsed.resource}', None)
    if task:
        task(parsed.name)
    else:
        print(f'{parsed.resource} invalid resource.')
        parser.print_help()

def _command(name):
    proj_root = Path().cwd()
    name = camel_to_snake(name)
    path = proj_root / 'commands' / f'{name}.py'
    if path.exists():
        raise ValueError(f'{path} already exists.')
    with open(path.as_posix(), 'w') as w:
        w.write(render_template('command.py.tpl', name=name))
    print(f'created: {path.as_posix()}')

def _controller(name):
    proj_root = Path().cwd()
    name = camel_to_snake(name)
    path = proj_root / 'controllers' / f'{name}.py'
    if path.exists():
        raise ValueError(f'{path} already exists.')
    with open(path.as_posix(), 'w') as w:
        w.write(render_template('controller.py.tpl'))
    print(f'created: {path.as_posix()}')

def _migration(name):
    # @TODO
    pass

def _model(name):
    # @TODO
    pass

