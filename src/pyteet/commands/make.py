from pyteet import camel_to_snake, render_template

import argparse
import importlib
from datetime import datetime, UTC
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
    proj_root = Path().cwd()
    prefix = datetime.now(UTC).strftime('%Y%m%d%H%M%S')
    name = f'{prefix}_{camel_to_snake(name)}'
    path = proj_root / 'migrations' / f'{name}.py'
    with open(path.as_posix(), 'w') as w:
        w.write(render_template('migration.py.tpl', name=name))
    print(f'created: {path.as_posix()}')

def _model(name):
    proj_root = Path().cwd()
    table = camel_to_snake(name)
    path = proj_root / 'models' / f'{table}.py'
    with open(path.as_posix(), 'w') as w:
        w.write(render_template('model.py.tpl', name=name, table=table))
    print(f'created: {path.as_posix()}')

