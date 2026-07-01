from pyteet import render_template

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
    app_ini_example = proj_root / 'app.ini.example'
    if not app_ini_example.exists():
        with open(app_ini_example.as_posix(), 'w') as w:
            w.write(render_template('app.ini'))
    app_py = proj_root / 'app.py'
    if not app_py.exists():
        with open(app_py.as_posix(), 'w') as w:
            w.write(render_template('app.py'))
    requirements = proj_root / 'requirements.txt'
    if not requirements.exists():
        with open(requirements.as_posix(), 'w') as w:
            w.write(render_template('requirements.txt'))
    requirements_mysql = proj_root / 'requirements-mysql.txt'
    if not requirements_mysql.exists():
        with open(requirements_mysql.as_posix(), 'w') as w:
            w.write(render_template('requirements-mysql.txt'))
    requirements_postgres = proj_root / 'requirements-postgres.txt'
    if not requirements_postgres.exists():
        with open(requirements_postgres.as_posix(), 'w') as w:
            w.write(render_template('requirements-postgres.txt'))
    commands = proj_root / 'commands'
    if not commands.exists():
        commands.mkdir()
    commands_init = proj_root / 'commands' / '__init__.py'
    if not commands_init.exists():
        with open(commands_init.as_posix(), 'w') as w:
            w.write(render_template('__init__.py'))
    controllers = proj_root / 'controllers'
    if not controllers.exists():
        controllers.mkdir()
    controllers_init = proj_root / 'controllers' / '__init__.py'
    if not controllers_init.exists():
        with open(controllers_init.as_posix(), 'w') as w:
            w.write(render_template('__init__.py'))
    controllers_home = proj_root / 'controllers' / 'home.py'
    if not controllers_home.exists():
        with open(controllers_home.as_posix(), 'w') as w:
            w.write(render_template('controller.py'))
    models = proj_root / 'models'
    if not models.exists():
        models.mkdir()
    models_init = proj_root / 'models' / '__init__.py'
    if not models_init.exists():
        with open(models_init.as_posix(), 'w') as w:
            w.write(render_template('__init__.py'))
