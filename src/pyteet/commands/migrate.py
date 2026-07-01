from pyteet import camel_to_snake, render_template

import argparse
import importlib
from pathlib import Path

NAME = 'migrate'
DESC = 'Database migration tasks'

def run(args):
    parser = argparse.ArgumentParser(
            description=DESC,
            usage=NAME)
    parser.add_argument(
            'task',
            help='run, rollback, status',
            type=str)
    parsed = parser.parse_args(args)
    module = importlib.import_module(__name__)
    task = getattr(module, f'_{parsed.task}', None)
    if task:
        task()
    else:
        print(f'{parsed.resource} invalid resource.')
        parser.print_help()

def _run():
    # @TODO
    pass

def _rollback():
    # @TODO
    pass

def _status():
    # @TODO
    pass

