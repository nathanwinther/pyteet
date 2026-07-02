from pyteet import migrations, render_template

import argparse
from datetime import datetime, UTC
from pathlib import Path

NAME = 'pat'
DESC = 'Install Personal Access Token migration and model'

def run(args):
    parser = argparse.ArgumentParser(
            description=DESC,
            usage=NAME)
    parser.add_argument(
            '-i',
            '--install',
            action='store_true',
            help='install')
    parsed = parser.parse_args(args)
    if parsed.install:
        state = migrations()
        installed = False
        for item in state:
            if item['migration'].endswith('_create_pyteet_pat'):
                print('hit:', item['migration'])
                installed = True
                break
        print(installed)
        if installed:
            print('installed:', installed)
            return
        # Install
        proj_root = Path().cwd()
        # Migration
        prefix = datetime.now(UTC).strftime('%Y%m%d%H%M%S')
        suffix = 'create_pyteet_pat'
        path = proj_root / 'migrations' / f'{prefix}_{suffix}.py'
        with open(path.as_posix(), 'w') as w:
            w.write(render_template(f'{suffix}.py.tpl', prefix=prefix))
        print(f'created: {path.as_posix()}')
        # Model
        name = 'personal_access_token'
        path = proj_root / 'models' / f'{name}.py'
        with open(path.as_posix(), 'w') as w:
            w.write(render_template(f'{name}.py.tpl'))
        print(f'created: {path.as_posix()}')
    else:
        parser.print_help()
