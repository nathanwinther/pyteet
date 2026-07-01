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
    # Include .gitignore
    gitignore = proj_root / '.gitignore'
    if not gitignore.exists():
        with open(gitignore.as_posix(), 'w') as w:
            w.write(render_template('gitignore.tpl'))
    # Include app.ini.example
    app_ini_example = proj_root / 'app.ini.example'
    if not app_ini_example.exists():
        with open(app_ini_example.as_posix(), 'w') as w:
            w.write(render_template('app.ini.tpl'))
    # Include app.py
    app_py = proj_root / 'app.py'
    if not app_py.exists():
        with open(app_py.as_posix(), 'w') as w:
            w.write(render_template('app.py.tpl'))
    # Include requirements
    requirements = proj_root / 'requirements.txt'
    if not requirements.exists():
        with open(requirements.as_posix(), 'w') as w:
            w.write(render_template('requirements.txt.tpl'))
    requirements_mysql = proj_root / 'requirements-mysql.txt'
    if not requirements_mysql.exists():
        with open(requirements_mysql.as_posix(), 'w') as w:
            w.write(render_template('requirements-mysql.txt.tpl'))
    requirements_postgres = proj_root / 'requirements-postgres.txt'
    if not requirements_postgres.exists():
        with open(requirements_postgres.as_posix(), 'w') as w:
            w.write(render_template('requirements-postgres.txt.tpl'))
    # Include commands
    commands = proj_root / 'commands'
    if not commands.exists():
        commands.mkdir()
    commands_init = proj_root / 'commands' / '__init__.py'
    if not commands_init.exists():
        with open(commands_init.as_posix(), 'w') as w:
            w.write(render_template('__init__.py.tpl'))
    # Include controllers
    controllers = proj_root / 'controllers'
    if not controllers.exists():
        controllers.mkdir()
    controllers_init = proj_root / 'controllers' / '__init__.py'
    if not controllers_init.exists():
        with open(controllers_init.as_posix(), 'w') as w:
            w.write(render_template('__init__.py.tpl'))
    # Include default controller
    controllers_home = proj_root / 'controllers' / 'home.py'
    if not controllers_home.exists():
        with open(controllers_home.as_posix(), 'w') as w:
            w.write(render_template('controller.py.tpl'))
    # Include migrations
    migrations = proj_root / 'migrations'
    if not migrations.exists():
        migrations.mkdir()
    migrate_init = proj_root / 'migrations' / '__init__.py'
    if not migrate_init.exists():
        with open(migrate_init.as_posix(), 'w') as w:
            w.write(render_template('__init__.py.tpl'))
    # Include models
    models = proj_root / 'models'
    if not models.exists():
        models.mkdir()
    models_init = proj_root / 'models' / '__init__.py'
    if not models_init.exists():
        with open(models_init.as_posix(), 'w') as w:
            w.write(render_template('__init__.py.tpl'))
    # Include templates
    templates = proj_root / 'templates'
    if not templates.exists():
        templates.mkdir()
