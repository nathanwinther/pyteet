from pyteet import database, migrations, render_template

import argparse
from datetime import datetime, UTC
from pathlib import Path

NAME = 'pat'
DESC = 'Install Personal Access Token migration'

def run(args):
    parser = argparse.ArgumentParser(
            description=DESC,
            usage=NAME)
    parser.add_argument(
            '-c',
            '--connection',
            default=None,
            help='database connection',
            type=str)
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
        if installed:
            print('installed:', installed)
            return
        # Install migration
        proj_root = Path().cwd()
        prefix = datetime.now(UTC).strftime('%Y%m%d%H%M%S')
        suffix = 'create_pyteet_pat'
        path = proj_root / 'migrations' / f'{prefix}_{suffix}.py'
        db = database(parsed.connection)
        with open(path.as_posix(), 'w') as w:
            w.write(render_template(
                f'migration_{db.driver}_create_pyteet_pat.py.tpl',
                prefix=prefix))
        print(f'created: {path.as_posix()}')
    else:
        parser.print_help()
