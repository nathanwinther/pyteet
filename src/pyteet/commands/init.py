from pyteet.util import render_pyteet_template

import argparse
from pathlib import Path

NAME = 'init'
DESC = 'Create a new pyteet project'

def run(args):
    parser = argparse.ArgumentParser(
            description=DESC,
            usage=NAME)
    parsed = parser.parse_args(args)
    proj_root = Path().cwd()
    # Include .gitignore
    gitignore = proj_root / '.gitignore'
    if not gitignore.exists():
        with open(gitignore.as_posix(), 'w') as w:
            w.write(render_pyteet_template('gitignore.tpl'))
            print(f'created: {gitignore.as_posix()}')
    # Include app.ini.example
    app_ini_example = proj_root / 'app.ini.example'
    if not app_ini_example.exists():
        with open(app_ini_example.as_posix(), 'w') as w:
            w.write(render_pyteet_template('app.ini.example.tpl'))
            print(f'created: {app_ini_example.as_posix()}')
    # Include app.py 
    app_py = proj_root / 'app.py'
    if not app_py.exists():
        with open(app_py.as_posix(), 'w') as w:
            w.write(render_pyteet_template('app.py.tpl'))
            print(f'created: {app_py.as_posix()}')
    # Include optional-requirements.txt
    requirements = proj_root / 'optional-requirements.txt'
    if not requirements.exists():
        with open(requirements.as_posix(), 'w') as w:
            w.write(render_pyteet_template('optional-requirements.txt.tpl'))
            print(f'created: {requirements.as_posix()}')
    # Include commands
    commands = proj_root / 'commands'
    if not commands.exists():
        commands.mkdir()
        print(f'created: {commands.as_posix()}')
    # Include controllers
    controllers = proj_root / 'controllers'
    if not controllers.exists():
        controllers.mkdir()
        print(f'created: {controllers.as_posix()}')
    # Include controllers/home.py
    controllers_home = proj_root / 'controllers' / 'home.py'
    if not controllers_home.exists():
        with open(controllers_home.as_posix(), 'w') as w:
            w.write(render_pyteet_template('controller.py.tpl'))
            print(f'created: {controllers_home.as_posix()}')
    # Include migrations
    migrations = proj_root / 'migrations'
    if not migrations.exists():
        migrations.mkdir()
        print(f'created: {migrations.as_posix()}')
    # Include models
    models = proj_root / 'models'
    if not models.exists():
        models.mkdir()
        print(f'created: {models.as_posix()}')
