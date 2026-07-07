import copy
import re
import threading
from pathlib import Path

from .log import Log
from .config import config
from .util import parsebool, parseint

DATETIME = '%Y-%m-%d %H:%M:%S'

_conn_pool = {}

def database(name:str | None = None) -> DBWrap:
    if not name:
        name = config('database.default')
        if not name:
            raise ValueError('database.default not defined.')
    conn_info = copy.deepcopy(config(name))
    if not conn_info:
        raise ValueError(f'{name} database not defined.')
    if not 'driver' in conn_info:
        raise ValueError(f'{name} does not define driver.')
    driver = conn_info['driver']
    if driver == 'mysql':
        return DBWrapMysql(name, driver, conn_info)
    if driver == 'postgres':
        return DBWrapPostgres(name, driver, conn_info)
    if driver == 'sqlite':
        return DBWrapSqlite(name, driver, conn_info)
    raise ValueError(f'{driver} driver not supported.')

def database_close():
    match = f'{threading.get_ident()}:'
    keys = [k for k in _conn_pool.keys() if k.startswith(match)]
    for k in keys:
        try:
            _conn_pool[k].close()
            Log.debug(message=f'closed database connection: {k}')
            del(_conn_pool[k])
        except:
            Log.error(error=f'close database connection failed: {k}')

def database_release():
    keys = [k for k in _conn_pool.keys()]
    for k in keys:
        del(_conn_pool[k])

class DBWrap:

    def __init__(self, name: str, driver: str, conn_info: dict):
        self.name = name
        self.driver = driver
        self.conn_info = conn_info

    def _fmt_sql(self, sql: str) -> str:
        sql = re.sub(r'\s\s*', ' ', sql)
        return sql.strip().strip(';')

    def _pool_add(self, conn):
        id = f'{threading.get_ident()}:{self.name}'
        Log.debug(f'Add connection to pool {id}:{conn}')
        _conn_pool[id] = conn

    def _pool_get(self):
        id = f'{threading.get_ident()}:{self.name}'
        if id in _conn_pool:
            conn = _conn_pool[id]
            Log.debug(f'Get connection from pool {id}:{conn}')
            return conn
        return False

class DBWrapMysql(DBWrap):
    def connect(self):
        import mysql.connector
        self.cursor_args = {'dictionary': True}
        conn = self._pool_get()
        if conn:
            return conn
        # Required
        params = {
                'host': self.conn_info['host'],
                'port': parseint(self.conn_info['port']),
                'database': self.conn_info['database'],
                'username': self.conn_info['username'],
                'password': self.conn_info['password'],
                }
        # Optional
        if 'autocommit' in self.conn_info:
            params['autocommit'] = parsebool(self.conn_info['autocommit'])
        else:
            params['autocommit'] = True
        if 'ssl_ca' in self.conn_info:
            path = Path().cwd() / self.conn_info['ssl_ca']
            if path.exists():
                params['ssl_ca'] = path.as_posix()
        if 'ssl_verify_identity' in self.conn_info:
            params['ssl_verify_identity'] = parsebool(
                    self.conn_info['ssl_verify_identity'])
        conn = mysql.connector.connect(**params)
        self._pool_add(conn)
        return conn

    def execute(self, sql: str, bind: tuple | None = None):
        try:
            conn = self.connect()
            with conn.cursor(**self.cursor_args) as cursor:
                sql = self._fmt_sql(sql)
                cursor.execute(sql, bind)
                Log.sql(sql=cursor.statement)
        except Exception as e:
            Log.error(error=e, sql=sql, bind=bind)
            raise e

    def fetchall(self, sql: str, bind: tuple | None = None) -> dict:
        try:
            conn = self.connect()
            with conn.cursor(**self.cursor_args) as cursor:
                sql = self._fmt_sql(sql)
                cursor.execute(sql, bind)
                Log.sql(sql=cursor.statement)
                return cursor.fetchall()
        except Exception as e:
            Log.error(error=e, sql=sql, bind=bind)
            raise e

    def fetchone(self, sql: str, bind: tuple | None = None) -> list:
        try:
            conn = self.connect()
            with conn.cursor(**self.cursor_args) as cursor:
                sql = self._fmt_sql(sql)
                cursor.execute(sql, bind)
                Log.sql(sql=cursor.statement)
                return cursor.fetchone()
        except Exception as e:
            Log.error(error=e, sql=sql, bind=bind)
            raise e

    def insert(self, sql: str, bind: tuple) -> int:
        try:
            conn = self.connect()
            with conn.cursor(**self.cursor_args) as cursor:
                sql = self._fmt_sql(sql)
                cursor.execute(sql, bind)
                Log.sql(sql=cursor.statement)
                return cursor.lastrowid
        except Exception as e:
            Log.error(error=e, sql=sql, bind=bind)
            raise e

class DBWrapPostgres(DBWrap):

    def connect(self):
        import psycopg
        from psycopg.rows import dict_row
        self.cursor_args = {'row_factory': dict_row}
        conn = self._pool_get()
        if conn:
            return conn
        # Required
        params = {
                'host': self.conn_info['host'],
                'port': parseint(self.conn_info['port']),
                'dbname': self.conn_info['database'],
                'user': self.conn_info['username'],
                'password': self.conn_info['password'],
                }
        # Optional
        autocommit = True
        if 'autocommit' in self.conn_info:
            autocommit = parsebool(self.conn_info['autocommit'])
        conn_str = ' '.join([f'{k}={v}' for k, v in params.items()])
        conn = psycopg.connect(conn_str, autocommit=autocommit)
        self._pool_add(conn)
        return conn

    def execute(self, sql: str, bind: tuple | None = None):
        try:
            conn = self.connect()
            with conn.cursor(**self.cursor_args) as cursor:
                sql = self._fmt_sql(sql)
                cursor.execute(sql, bind)
                Log.sql(sql=sql, bind=bind)
        except Exception as e:
            Log.error(error=e, sql=sql, bind=bind)
            raise e

    def fetchall(self, sql: str, bind: tuple | None = None) -> dict:
        try:
            conn = self.connect()
            with conn.cursor(**self.cursor_args) as cursor:
                sql = self._fmt_sql(sql)
                cursor.execute(sql, bind)
                Log.sql(sql=sql, bind=bind)
                return cursor.fetchall()
        except Exception as e:
            Log.error(error=e, sql=sql, bind=bind)
            raise e

    def fetchone(self, sql: str, bind: tuple | None = None) -> list:
        try:
            conn = self.connect()
            with conn.cursor(**self.cursor_args) as cursor:
                sql = self._fmt_sql(sql)
                cursor.execute(sql, bind)
                Log.sql(sql=sql, bind=bind)
                return cursor.fetchone()
        except Exception as e:
            Log.error(error=e, sql=sql, bind=bind)
            raise e

    def insert(self, sql: str, bind: tuple) -> int:
        try:
            conn = self.connect()
            with conn.cursor(**self.cursor_args) as cursor:
                sql = self._fmt_sql(sql)
                cursor.execute(sql, bind)
                Log.sql(sql=sql, bind=bind)
                result = cursor.fetchone()
                return list(result.values()).pop(0)
        except Exception as e:
            Log.error(error=e, sql=sql, bind=bind)
            raise e

class DBWrapSqlite(DBWrap):

    def connect(self):
        import sqlite3
        autocommit=True
        if 'autocommit' in self.conn_info:
            autocommit = parsebool(self.conn_info['autocommit'])
        conn = sqlite3.connect(
                self.conn_info['database'], 
                autocommit=autocommit)
        conn.row_factory = sqlite3.Row
        return conn

    def execute(self, sql: str, bind: tuple | None = None):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                sql = self._fmt_sql(sql)
                bind = bind if bind else ()
                cursor.execute(sql, bind)
                Log.sql(sql=sql, bind=bind)
        except Exception as e:
            Log.error(error=e, sql=sql, bind=bind)
            raise e

    def fetchall(self, sql: str, bind: tuple | None = None) -> dict:
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                sql = self._fmt_sql(sql)
                bind = bind if bind else ()
                cursor.execute(sql, bind)
                Log.sql(sql=sql, bind=bind)
                rows = cursor.fetchall()
                rows = [dict(v) for v in rows]
                return rows
        except Exception as e:
            Log.error(error=e, sql=sql, bind=bind)
            raise e

    def fetchone(self, sql: str, bind: tuple | None = None) -> list:
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                sql = self._fmt_sql(sql)
                bind = bind if bind else ()
                cursor.execute(sql, bind)
                Log.sql(sql=sql, bind=bind)
                row = cursor.fetchone()
                return dict(row) if row else None
        except Exception as e:
            Log.error(error=e, sql=sql, bind=bind)
            raise e

    def insert(self, sql: str, bind: tuple) -> int:
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                sql = self._fmt_sql(sql)
                bind = bind if bind else ()
                cursor.execute(sql, bind)
                Log.sql(sql=sql, bind=bind)
                return cursor.lastrowid
        except Exception as e:
            Log.error(error=e, sql=sql, bind=bind)
            raise e

    def _fmt_sql(self, sql: str) -> str:
        sql = re.sub('%s', '?', sql)
        return super()._fmt_sql(sql)

