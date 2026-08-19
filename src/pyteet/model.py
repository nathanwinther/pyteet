from .database import DATETIME
from .database import database

import copy
from datetime import datetime
from datetime import UTC

class Model:

    # MUST DEFINE
    TABLE = 'your_table'
    PRIMARY_KEY = 'id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    CONNECTION = None # Use default database connection

    # Model data for DB mapping
    _data = {}
    # Model data that has been modified and unsaved
    _dirty = []

    def __init_subclass__(cls):
        super().__init_subclass__()
        if not hasattr(cls, 'TABLE'):
            raise TypeError(f'{cls.__name__} must define attribute TABLE')
        if not hasattr(cls, 'PRIMARY_KEY'):
            raise TypeError(f'{cls.__name__} must define attribute PRIMARY_KEY')
        if not hasattr(cls, 'CREATED_AT'):
            raise TypeError(f'{cls.__name__} must define attribute CREATED_AT')
        if not hasattr(cls, 'UPDATED_AT'):
            raise TypeError(f'{cls.__name__} must define attribute UPDATED_AT')
        if not hasattr(cls, 'CONNECTION'):
            raise TypeError(f'{cls.__name__} must define attribute CONNECTION')

    def __init__(self):
        self._data = {}
        self._dirty = []

    def __getattr__(self, name: str) -> any:
        # Method missing hook
        return self._data.get(name)

    def __setattr__(self, name: str, value: any):
        if hasattr(type(self), name):
            # Normal set
            super().__setattr__(name, value)
        else:
            self.set(name, value)

    def creating(self):
        '''Called on save() for INSERT.'''
        pass

    def data(self) -> dict:
        return copy.deepcopy(self._data)

    def dirty(self) -> list:
        return copy.deepcopy(self._dirty)

    def fill(self, data: dict):
        for k, v in data.items():
            self.set(k, v)

    def find(self, id: int) -> Model:
        sql = f'''
            SELECT
                *
            FROM {self.TABLE}
            WHERE `{self.PRIMARY_KEY}` = %s
        '''
        data = database(self.CONNECTION).fetchone(sql, (id, ))
        if not data:
            return None
        inst = self.__class__()
        inst._data = data
        return inst

    def fetchall(self, sql: str, bind: tuple | None=None) -> list:
        rows = database(self.CONNECTION).fetchall(sql, bind)
        if not rows:
            return []
        for k, v in enumerate(rows):
            inst = self.__class__()
            inst._data = v
            rows[k] = inst
        return rows

    def fetchone(self, sql: str, bind: tuple | None=None) -> Model:
        data = database(self.CONNECTION).fetchone(sql, bind)
        if not data:
            return None
        inst = self.__class__()
        inst._data = data
        return inst

    def for_api(self, data: any | None=None) -> any:
        if not data:
            data = self.data()
        return data

    def get(self, name: str, default: any | None=None) -> any:
        return self._data.get(name, default)

    def is_dirty(self, name: str | None=None):
        if name:
            return name in self._dirty
        return len(self._dirty) > 0

    def save(self):
        if not self._dirty:
            # Nothing to save
            return
        pk = getattr(self, self.PRIMARY_KEY)
        dt = datetime.now(UTC).strftime(DATETIME)
        db = database(self.CONNECTION)
        is_insert = pk == None
        if is_insert:
            self.creating()
            if self.CREATED_AT:
                setattr(self, self.CREATED_AT, dt)
        self.saving()
        if self.UPDATED_AT:
            setattr(self, self.UPDATED_AT, dt)
        payload = {}
        for k in self._dirty:
            payload[k] = self._data.get(k)
        keys = list(payload.keys())
        values = tuple([payload[k] for k in keys])
        if is_insert:
            sql = '''
                INSERT INTO {} ({})
                VALUES ({})
            '''.format(self.TABLE,
                       ', '.join([f'`{x}`' for x in keys]),
                       ', '.join(['%s'] * len(values)))
            if db.driver == 'postgres':
                sql += '''
                    RETURNING {}
                '''.format(self.PRIMARY_KEY)
            pk = db.insert(sql, values)
            setattr(self, self.PRIMARY_KEY, pk)
            self._dirty = []
            return
        else:
            sql = '''
                UPDATE {}
                SET {}
                WHERE `{}` = %s
            '''.format(self.TABLE,
                       ', '.join([f'`{x}` = %s' for x in keys]),
                       self.PRIMARY_KEY)
            values += (pk, )
            db.execute(sql, values)
            self._dirty = []
            return

    def saving(self):
        '''Called on save() for INSERT and UPDATE.'''
        pass

    def set(self, name: str, value: any):
        # Trim strings
        if isinstance(value, str):
            value = value.strip()
        # Changed?
        if self._data.get(name) == value:
            # No change
            return
        # Set
        self._data[name] = value
        # Is dirty
        if not name in self._dirty:
            # Mark as dirty
            self._dirty.append(name)

