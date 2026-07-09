from pyteet import camel_to_snake, pluralize, render_template

import argparse
from datetime import datetime, UTC
from pathlib import Path

NAME = 'make'
DESC = 'Create a new resource'
LONG_DESC = '''Create a new resource

Commands

command    [name] module name Ex. process_orders
controller [name] module name Ex. orders
migration  [name] module name Ex. create_orders
model      [name] class name  Ex. OrderDetail
'''

def run(args):
    parser = argparse.ArgumentParser(
            description=LONG_DESC,
            exit_on_error=False,
            formatter_class=argparse.RawTextHelpFormatter,
            usage=NAME)
    parser.add_argument(
            'command',
            help='command',
            type=str)
    parser.add_argument(
            'name',
            help='resource name',
            type=str)
    try:
        parsed = parser.parse_args(args)
        command = globals().get(f'_{parsed.command}')
        command(parsed.name)
    except:
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
    file = camel_to_snake(name)
    table = pluralize(file)
    path = proj_root / 'models' / f'{file}.py'
    with open(path.as_posix(), 'w') as w:
        w.write(render_template('model.py.tpl', name=name, table=table))
    print(f'created: {path.as_posix()}')

