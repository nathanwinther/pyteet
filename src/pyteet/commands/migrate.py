from pyteet import DATETIME, database, migrations, parseint, Log

import argparse
import importlib
from datetime import datetime, UTC
from functools import reduce

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
    task = globals().get(f'_{parsed.task}')
    if task and callable(task):
        if parsed.task == 'rollback':
            task(parsed.connection, parsed.batch)
        else:
            task(parsed.connection)
    else:
        print(f'{parsed.task} invalid task.')
        parser.print_help()

def _run(connection):
    state = migrations(connection)
    unprocessed = [item for item in state if item['processed'] == False]
    if not unprocessed:
        return
    db = database(connection)
    dt = datetime.now(UTC).strftime(DATETIME)
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
    state = migrations(connection)
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
    state = migrations(connection)
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

