from pyteet import DATETIME_DB, database, parseint, Log

import argparse
import importlib
import json
from datetime import datetime, UTC
from functools import reduce
from operator import itemgetter
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
    parser.add_argument(
            '-c',
            '--connection',
            default=None,
            help='database connection',
            type=str)
    parser.add_argument(
            '-b',
            '--batch',
            default=None,
            help='batch id for rollback',
            type=int)
    parsed = parser.parse_args(args)
    module = importlib.import_module(__name__)
    task = getattr(module, f'_{parsed.task}', None)
    if task:
        if task == 'rollback':
            task(parsed.connection, parsed.batch)
        else:
            task(parsed.connection)
    else:
        print(f'{parsed.task} invalid task.')
        parser.print_help()

def _run(connection):
    state = _migrations(connection)
    unprocessed = [item for item in state if item['processed'] == False]
    if not unprocessed:
        return
    db = database(connection)
    dt = datetime.now(UTC).strftime(DATETIME_DB)
    def _max_batch(acc, item):
        batch = parseint(item.get('batch', ''))
        return batch if batch > acc else acc
    max_batch = reduce(_max_batch, state, 0)
    for item in unprocessed:
        migration = item['migration']
        print(f'{migration} migration started')
        module = importlib.import_module(item['module'])
        getattr(module, 'migrate')()
        sql = '''
            INSERT INTO pyteet_migrations
            (migration, batch, created_at, updated_at)
            VALUES(%s, %s, %s, %s)
        '''
        db.execute(sql, (migration, max_batch + 1, dt, dt))
        print(f'{migration} migration complete')

def _rollback(connection, batch=None):
    state = _migrations(connection)
    if not batch:
        def _max_batch(acc, item):
            batch = parseint(item.get('batch', ''))
            return batch if batch > acc else acc
        batch = reduce(_max_batch, state, 0)
    if not batch:
        return
    db = database(connection)
    sql = '''
        SELECT
        *
        FROM pyteet_migrations
        WHERE batch = %s
    '''
    rows = db.fetchall(sql, (batch, ))
    for row in rows:
        migration = row['migration']
        print(f'{migration} rollback started')
        module = importlib.import_module(f'migrations.{migration}')
        getattr(module, 'rollback')()
        print(f'{migration} rollback complete')
    sql = '''
        DELETE FROM pyteet_migrations
        WHERE batch = %s
    '''
    db.execute(sql, (batch, ))

def _status(connection):
    def print_sep(max_len):
        print('{}{}{}{}{}{}{}'.format(
            '+-',
            '-' * max_len[0],
            '-+-',
            '-' * max_len[1],
            '-+-',
            '-' * max_len[2],
            '-+'))
    def print_row(row, max_len):
        print('{}{}{}{}{}{}{}'.format(
            '| ',
            row[0].ljust(max_len[0]),
            ' | ',
            row[1].ljust(max_len[1]),
            ' | ',
            row[2].ljust(max_len[2]),
            ' |'))
    state = _migrations(connection)
    header = ['Ran?', 'Migration', 'Batch']
    max_len = [len(x) for x in header]
    for k, v in enumerate(state):
        len_mgrtn = len(v['migration'])
        max_len[1] = len_mgrtn if len_mgrtn > max_len[1] else max_len[1]
        len_batch = len(str(v['batch']))
        max_len[2] = len_batch if len_batch > max_len[2] else max_len[2]
        state[k] = [
                'Yes' if v['processed'] else 'No',
                v['migration'],
                str(v['batch']),
                ]
    print_sep(max_len)
    print_row(header, max_len)
    print_sep(max_len)
    if state:
        for row in state:
            print_row(row, max_len)
        print_sep(max_len)

def _migrations(connection):
    def find(state, migration):
        for idx, item in enumerate(state):
            if item['migration'] == migration:
                return idx
        return -1
    def validate(module):
        must_have = ('NAME', 'CONNECTION', 'migrate', 'rollback')
        for k in must_have:
            if not hasattr(module, k):
                return False
        return True
    # Get migrations
    state = []
    db = database(connection)
    try:
        sql = '''
            SELECT
            *
            FROM pyteet_migrations
        '''
        state = database(connection).fetchall(sql)
    except:
        Log.debug(f'pyteet_migrations does not exist, create.')
        if db.driver == 'mysql':
            sql = '''
                CREATE TABLE pyteet_migrations (
                    id bigint unsigned NOT NULL AUTO_INCREMENT,
                    migration varchar(255) NOT NULL,
                    batch bigint unsigned NOT NULL,
                    created_at timestamp NULL DEFAULT NULL,
                    updated_at timestamp NULL DEFAULT NULL,
                    PRIMARY KEY (id)
                )
            '''
        if db.driver == 'postgres':
            sql = '''
                CREATE TABLE pyteet_migrations (
                    id bigint PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
                    migration varchar(255) NOT NULL,
                    batch bigint NOT NULL,
                    created_at timestamp NULL DEFAULT NULL,
                    updated_at timestamp NULL DEFAULT NULL
                )
            '''
        if db.driver == 'sqlite':
            sql = '''
                CREATE TABLE pyteet_migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    migration TEXT NOT NULL,
                    batch INTEGER NOT NULL,
                    created_at TEXT NULL,
                    updated_at TEXT NULL
                )
            '''
        db.execute(sql)
    # Find migrations
    path = Path().cwd() / 'migrations'
    if path.exists():
        for file in path.iterdir():
            if not file.is_file():
                continue
            if file.suffix != '.py':
                continue
            module_name = f'migrations.{file.stem}'
            module = importlib.import_module(module_name)
            if not validate(module):
                continue
            migration = getattr(module, 'NAME')
            idx = find(state, migration)
            if idx >= 0:
                state[idx]['processed'] = True
            else:
                state.append({
                    'id': '',
                    'migration': migration,
                    'batch': '',
                    'processed': False,
                    'module': module_name,
                    })
    state = sorted(state, key=itemgetter('migration'))
    return state

